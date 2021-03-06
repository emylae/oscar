from django.shortcuts import render
from django.db.models import Count

from .utils import user_is_superuser

from promotions.models import Professor, Student, Lesson, Stage
from skills.models import Skill, KhanAcademyVideoSkill, SesamathSkill

from examinations.models import Exercice as Question


@user_is_superuser
def dashboard(request):
    questions_per_stage = []
    for stage in Stage.objects.annotate(Count("skills"), Count("skills__exercice")):
        skills = stage.skills_with_exercice_count()
        print stage.skills__exercice__count
        questions_per_stage.append({
            "stage": stage,
            "skills_count_with_questions": skills.filter(exercice__count__gt=0),
            # "skills_count_without_questions": skills.filter(exercice__count=0),
        })


    return render(request, "stats/dashboard.haml", {
        "professors": Professor.objects.all(),
        "students": Student.objects.all(),
        "lessons": Lesson.objects.all(),
        "skills": Skill.objects.all(),
        "skills_with_khan_ressources": Skill.objects.annotate(Count('khanacademyvideoskill')).filter(khanacademyvideoskill__count__gt=0),
        "skills_with_sesamath_ressources": Skill.objects.annotate(Count('sesamathskill')).filter(sesamathskill__count__gt=0),
        "khanacademyvideoskill": KhanAcademyVideoSkill.objects.order_by('-created_at').select_related('skill', 'reference'),
        "sesamathskill": SesamathSkill.objects.order_by('-created_at').select_related('skill', 'reference'),
        "questions": Question.objects.all(),
        "stages_with_skills_with_questions": questions_per_stage,
        "skills_with_questions": Skill.objects.annotate(Count('exercice')).filter(exercice__count__gt=0),
    })
