# coding: utf-8
import urllib

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST
from django.template.response import TemplateResponse
from django.conf import settings

from oioioi.base.utils import tabbed_view, jsonify
from oioioi.base.utils.redirect import safe_redirect
from oioioi.problems.models import ProblemStatement, ProblemAttachment, \
        Problem, ProblemPackage, Tag
from oioioi.filetracker.utils import stream_file
from oioioi.problems.utils import can_admin_problem, \
        query_statement, can_admin_instance_of_problem, \
        can_admin_problem_instance, can_add_to_problemset
from oioioi.problems.problem_sources import problem_sources
from oioioi.problems.problem_site import problem_site_tab_registry
from oioioi.contests.models import Submission, SubmissionReport, \
        ProblemInstance
from oioioi.contests.processors import recent_contests
from oioioi.contests.utils import is_contest_admin, administered_contests
from oioioi.contests.middleware import activate_contest
from oioioi.programs.models import ModelSolution, TestReport, GroupReport, \
        ModelProgramSubmission
from oioioi.problems.forms import ProblemsetSourceForm

from collections import defaultdict

# problem_site_statement_zip_view is used in one of the tabs
# in problem_site.py. We placed the view in problem_site.py
# instead of views.py to avoid circular imports. We still import
# it here to use it in urls.py.
from oioioi.problems.problem_site import problem_site_statement_zip_view


def show_statement_view(request, statement_id):
    statement = get_object_or_404(ProblemStatement, id=statement_id)
    if not can_admin_instance_of_problem(request, statement.problem):
        raise PermissionDenied
    return stream_file(statement.content, statement.download_name)


def show_problem_attachment_view(request, attachment_id):
    attachment = get_object_or_404(ProblemAttachment, id=attachment_id)
    if not can_admin_instance_of_problem(request, attachment.problem):
        raise PermissionDenied
    return stream_file(attachment.content, attachment.download_name)


def _get_package(request, package_id):
    package = get_object_or_404(ProblemPackage, id=package_id)
    has_perm = False
    if package.contest:
        has_perm = request.user.has_perm('contests.contest_admin',
                package.contest)
    elif package.problem:
        has_perm = can_admin_problem(request, package.problem)
    else:
        has_perm = request.user.is_superuser
    if not has_perm:
        raise PermissionDenied
    return package


def download_problem_package_view(request, package_id):
    package = _get_package(request, package_id)
    return stream_file(package.package_file, package.download_name)


def download_package_traceback_view(request, package_id):
    package = _get_package(request, package_id)
    if not package.traceback:
        raise Http404
    return stream_file(package.traceback, 'package_%s_%d_traceback.txt' % (
            package.problem_name, package.id))


# This generates all metadata needed for
# "add to contest" functionality in problemset.
def _generate_add_to_contest_metadata(request):
    administered = administered_contests(request)
    # If user doesn't own any contest we won't show the option.
    if administered:
        show_add_button = True
    else:
        show_add_button = False
    # We want to show administered recent contests, because
    # these are most likely to be picked by an user.
    rcontests = recent_contests(request)
    administered_recent_contests = None
    if rcontests:
        administered_recent_contests = \
            [contest
             for contest in rcontests
             if request.user.has_perm('contests.contest_admin', contest)]
    return show_add_button, administered_recent_contests


def add_or_update_problem(request, contest, template):
    if 'problem' in request.GET:
        existing_problem = \
                get_object_or_404(Problem, id=request.GET['problem'])
        if contest and not existing_problem.probleminstance_set.filter(
                contest=contest).exists():
            raise Http404
        if not can_admin_problem(request, existing_problem):
            raise PermissionDenied
    else:
        existing_problem = None
        if not request.user.has_perm('problems.problems_db_admin'):
            if contest and (not is_contest_admin(request)):
                raise PermissionDenied

    context = {'existing_problem': existing_problem}
    tab_kwargs = {
        'contest': contest,
        'existing_problem': existing_problem
    }

    tab_link_params = request.GET.dict()

    def build_link(tab):
        tab_link_params['key'] = tab.key
        return request.path + '?' + urllib.urlencode(tab_link_params)

    return tabbed_view(request, template, context,
            problem_sources(request), tab_kwargs, build_link)


@transaction.non_atomic_requests
def add_or_update_problem_view(request):
    return add_or_update_problem(request, request.contest,
                                 'problems/add-or-update.html')


def get_problem_queryset_by_tag(datadict):
    try:
        tag_name = datadict['tag_search']
        if not tag_name:
            return Problem.objects, ''
        tag = Tag.objects.get(name=tag_name)
        return tag.problems, tag_name
    except KeyError:
        return Problem.objects, ''
    except Tag.DoesNotExist:
        return Problem.objects.none(), ''


def problemset_generate_view(request, page_title, problems):
    # We want to show "Add to contest" button only
    # if user is contest admin for any contest.
    queryset, query_string = get_problem_queryset_by_tag(request.GET)
    show_add_button, administered_recent_contests = \
        _generate_add_to_contest_metadata(request)
    form = ProblemsetSourceForm("")

    return TemplateResponse(request,
       'problems/problemset/problem-list.html',
      {'problems': problems,
       'page_title': page_title,
       'select_problem_src': request.GET.get('select_problem_src'),
       'tag_search': query_string,
       'show_tags': getattr(settings, 'PROBLEM_TAGS_VISIBLE', False),
       'show_search_bar': True,
       'show_add_button': show_add_button,
       'administered_recent_contests': administered_recent_contests,
       'form': form})


def problemset_main_view(request):
    page_title = \
        _("Welcome to problemset, the place where all the problems are.")
    queryset = get_problem_queryset_by_tag(request.GET)[0]
    problems = queryset.filter(is_public=True, problemsite__isnull=False) \
        .order_by('name')

    return problemset_generate_view(request, page_title, problems)


def problemset_my_problems_view(request):
    page_title = _("My problems")
    queryset, query_string = get_problem_queryset_by_tag(request.GET)
    problems = queryset.filter(author=request.user, problemsite__isnull=False)\
        .order_by('name')

    return problemset_generate_view(request, page_title, problems)


def problemset_all_problems_view(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    page_title = _("All problems")
    queryset, query_string = get_problem_queryset_by_tag(request.GET)
    problems = queryset.filter(problemsite__isnull=False).order_by('name')

    return problemset_generate_view(request, page_title, problems)


def problem_site_view(request, site_key):
    problem = get_object_or_404(Problem, problemsite__url_key=site_key)
    package = ProblemPackage.objects.filter(problem=problem).first()
    show_add_button, administered_recent_contests = \
        _generate_add_to_contest_metadata(request)
    context = {'problem': problem,
               'package': package if package and package.package_file
                        else None,
               'can_admin_problem': can_admin_problem(request, problem),
               'select_problem_src': request.GET.get('select_problem_src'),
               'show_add_button': show_add_button,
               'administered_recent_contests': administered_recent_contests}
    tab_kwargs = {'problem': problem}

    tab_link_params = request.GET.dict()
    if 'page' in tab_link_params:
        del tab_link_params['page']

    def build_link(tab):
        tab_link_params['key'] = tab.key
        return request.path + '?' + urllib.urlencode(tab_link_params)

    return tabbed_view(request, 'problems/problemset/problem-site.html',
            context, problem_site_tab_registry, tab_kwargs, build_link)


def problem_site_external_statement_view(request, site_key):
    problem = get_object_or_404(Problem, problemsite__url_key=site_key)
    statement = query_statement(problem.id)
    if statement.extension == '.zip' \
            and not can_admin_problem(request, problem):
        raise PermissionDenied
    return stream_file(statement.content, statement.download_name)


def problem_site_external_attachment_view(request, site_key, attachment_id):
    problem = get_object_or_404(Problem, problemsite__url_key=site_key)
    attachment = get_object_or_404(ProblemAttachment, id=attachment_id)
    if attachment.problem.id != problem.id:
        raise PermissionDenied
    return stream_file(attachment.content, attachment.download_name)


def problemset_add_to_contest_view(request, site_key):
    problem_name = request.GET.get('problem_name')
    if not problem_name:
        raise Http404
    administered = administered_contests(request)
    administered = sorted(administered,
        key=lambda x: x.creation_date, reverse=True)
    return TemplateResponse(request, 'problems/problemset/select-contest.html',
                            {'site_key': site_key,
                             'administered_contests': administered,
                             'problem_name': problem_name})


def get_report_HTML_view(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    controller = submission.problem_instance.controller
    if not controller.filter_my_visible_submissions(request, Submission.objects
                            .filter(id=submission_id)).exists():
        raise Http404
    reports = ''
    queryset = SubmissionReport.objects.filter(submission=submission). \
        prefetch_related('scorereport_set')
    for report in controller.filter_visible_reports(request, submission,
            queryset.filter(status='ACTIVE')):
        reports += controller.render_report(request, report)

    if not reports:
        reports = _(u"Reports are not available now (ಥ ﹏ ಥ)")
        reports = mark_safe('<center>' + reports + '</center>')
    return HttpResponse(reports)


@transaction.non_atomic_requests
def problemset_add_or_update_problem_view(request):
    if not can_add_to_problemset(request):
        if request.contest:
            url = reverse('add_or_update_problem') + '?' + urllib \
                .urlencode(request.GET.dict())
            return safe_redirect(request, url)
        raise PermissionDenied

    return add_or_update_problem(request, None,
                                 'problems/problemset/add-or-update.html')


def model_solutions_view(request, problem_instance_id):
    problem_instance = \
        get_object_or_404(ProblemInstance, id=problem_instance_id)
    if not can_admin_problem_instance(request, problem_instance):
        raise PermissionDenied

    filter_kwargs = {
        'test__isnull': False,
        'submission_report__submission__problem_instance':
            problem_instance,
        'submission_report__submission__programsubmission'
                '__modelprogramsubmission__isnull': False,
        'submission_report__status': 'ACTIVE',
    }
    test_reports = TestReport.objects.filter(**filter_kwargs) \
            .select_related()
    filter_kwargs = {
        'submission_report__submission__problem_instance':
            problem_instance,
        'submission_report__submission__programsubmission'
                '__modelprogramsubmission__isnull': False,
        'submission_report__status': 'ACTIVE',
    }
    group_reports = GroupReport.objects.filter(**filter_kwargs) \
            .select_related()
    submissions = ModelProgramSubmission.objects \
            .filter(problem_instance=problem_instance) \
            .order_by('model_solution__order_key') \
            .select_related('model_solution') \
            .all()
    tests = problem_instance.test_set \
            .order_by('order', 'group', 'name').all()

    group_results = defaultdict(lambda: defaultdict(lambda: None))
    for gr in group_reports:
        group_results[gr.group][gr.submission_report.submission_id] = gr

    test_results = defaultdict(lambda: defaultdict(lambda: None))
    for tr in test_reports:
        test_results[tr.test_id][tr.submission_report.submission_id] = tr

    submissions_percentage_statuses = {s.id: '25' for s in submissions}
    rows = []
    submissions_row = []
    for t in tests:
        row_test_results = test_results[t.id]
        row_group_results = group_results[t.group]
        percentage_statuses = {s.id: '100' for s in submissions}
        for s in submissions:
            if row_test_results[s.id] is not None:
                time_ratio = float(row_test_results[s.id].time_used) / \
                        row_test_results[s.id].test_time_limit
                if time_ratio <= 0.25:
                    percentage_statuses[s.id] = '25'
                elif time_ratio <= 0.50:
                    percentage_statuses[s.id] = '50'
                    if submissions_percentage_statuses[s.id] is not '100':
                        submissions_percentage_statuses[s.id] = '50'
                else:
                    percentage_statuses[s.id] = '100'
                    submissions_percentage_statuses[s.id] = '100'

        rows.append({
            'test': t,
            'results': [
                {
                    'test_report': row_test_results[s.id],
                    'group_report': row_group_results[s.id],
                    'is_partial_score': s.problem_instance.controller
                                        ._is_partial_score(
                                            row_test_results[s.id]
                                        ),
                    'percentage_status': percentage_statuses[s.id]}
                for s in submissions]
        })

    for s in submissions:
        status = s.status
        if s.status == 'OK' or s.status == 'INI_OK':
            status = 'OK' + submissions_percentage_statuses[s.id]

        submissions_row.append({
            'submission': s,
            'status': status
            })

    total_row = {
        'test': sum(t.time_limit for t in tests),
        'results':
            [sum(t[s.id].time_used if t[s.id] else 0
                 for t in test_results.values())
             for s in submissions],
    }

    context = {
            'problem_instance': problem_instance,
            'submissions_row': submissions_row,
            'submissions': submissions,
            'rows': rows,
            'total_row': total_row
    }

    return TemplateResponse(request, 'programs/admin/model_solutions.html',
            context)


def rejudge_model_solutions_view(request, problem_instance_id):
    problem_instance = \
            get_object_or_404(ProblemInstance, id=problem_instance_id)
    contest = problem_instance.contest
    if not request.user.has_perm('contests.contest_admin', contest):
        raise PermissionDenied
    ModelSolution.objects.recreate_model_submissions(problem_instance)
    messages.info(request, _("Model solutions sent for evaluation."))
    return redirect('model_solutions', problem_instance.id)


@jsonify
def get_tag_hints_view(request):
    substr = request.GET.get('substr', '')
    if len(substr) < 2:
        raise Http404
    num_hints = getattr(settings, 'NUM_HINTS', 10)
    queryset = Tag.objects.filter(name__icontains=substr)[:num_hints].all()
    return [str(tag.name) for tag in queryset]
