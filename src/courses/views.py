from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, View

from memberships.models import UserMembership
from .models import Course

class CourseListView(ListView):
    model = Course

class CourseDetailView(DetailView):
    model = Course

class LessonDetailView(View):
    
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):

        # course query set
        course_qs = Course.objects.filter(slug=course_slug)
        if course_qs.exists():
            course = course_qs.first()

        lesson_qs = course.lessons.filter(slug=lesson_slug)
        if lesson_qs.exists():
            lesson = lesson_qs.first()

        user_membership = UserMembership.objects.filter(user=request.user).first()
        user_membership_type = user_membership.membership.membership_type

        course_allowed_mem_types = course.allowed_memberships.all()
    
        context = {
            'object': None,
        }

        if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
            context = {'object': lesson}

        return render(request, "courses/lesson_detail.html", context)