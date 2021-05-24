from dataclasses import dataclass
import sqlite3
from typing import List, Dict, Set
from collections import defaultdict


@dataclass
class Skill:
    name: str
    experience: int = None

    def __str__(self):
        return f"Has {self.experience}-year experience in {self.name}"


@dataclass
class Person:
    age: int
    first_name: str
    last_name: str
    phone_number: str
    company_name: str
    skills: [Skill]


def __select_persons_query__(skill: Skill):
    query_params = []
    if not skill.name and not skill.experience:
        return None

    skill_name_condition = "" if not skill.name else "S.name LIKE ? "
    if skill.name:
        if skill.name.startswith('\'') and skill.name.endswith('\''):
            query_params += [f"{skill.name[1:-1]}"]
        else:
            query_params += [f"%{skill.name}%"]

    skill_experience_condition = "" if not skill.experience \
        else "ES.experience >= ? "
    if skill.experience:
        query_params += [skill.experience]

    if skill_name_condition and skill_experience_condition:
        return f"""({skill_name_condition} AND {skill_experience_condition})""", query_params
    else:
        return f"""({skill_name_condition}{skill_experience_condition})""", query_params


class CandidatesRequestHandler:
    __candidates_db_name__ = 'candidates.db'

    __select_candidate_query__ = """
    SELECT * FROM Employee
    LEFT JOIN EmployeeSkill ES on Employee.id = ES.employeeId
    LEFT JOIN Skill S on S.id = ES.skillId
    LEFT JOIN CurrentWorkplace CW on Employee.id = CW.employeeId
    LEFT JOIN WorkPlace WP on WP.id = CW.workPlaceId
    """

    @staticmethod
    def get_candidates(age_range: range = None,
                       # male - 0, female - 1
                       gender=None,
                       required_skills: List[Skill] = None,
                       is_currently_employed=None,
                       has_higher_education=None,
                       ) -> [Person]:
        if required_skills is None:
            required_skills = []

        query_conditions = []
        query_params = []
        skills_set: Set[str] = set()
        for req_skill in required_skills:
            if req_skill.name and req_skill.name in skills_set:
                continue

            skills_set.add(req_skill.name)
            condition = __select_persons_query__(req_skill)

            if condition:
                query_params += condition[1]
                query_conditions.append(condition[0])

        query = "WHERE ("

        for condition in query_conditions:
            query += condition
            query += " OR "

        query += f" {len(query) <= 7} ) "

        if age_range:
            query_params.append(age_range.start)
            query_params.append(age_range.stop)
            query += " AND (age >= ? AND age <= ?) "

        if gender:
            query_params.append(gender)
            query += "AND (gender  = ?) "

        if is_currently_employed:
            query += "AND (workPlaceId != 0 ) "
        elif not is_currently_employed is None:
            query += "AND (workPlaceId = 0 ) "

        if not has_higher_education is None:
            query += "AND (hasHigherEducation = ?) "
            query_params.append(1 if has_higher_education else 0)

        connection = sqlite3.connect(CandidatesRequestHandler.__candidates_db_name__)

        cursor = connection.cursor()
        query = CandidatesRequestHandler.__select_candidate_query__ + query
        cursor.execute(query, query_params)
        values = cursor.fetchall()
        cursor.close()
        connection.close()

        candidates: Dict[int, Person] = CandidatesRequestHandler.__parse_data__(values)

        appropriate_candidates = []

        for candidate in candidates.values():
            if len(skills_set) <= len(candidate.skills):
                appropriate_candidates.append(candidate)
        return appropriate_candidates

    @staticmethod
    def __parse_data__(values):
        dict_person: Dict[int, Person] = defaultdict()
        for person in values:
            person_id = person[0]
            skills = [] if not dict_person.get(person_id) else dict_person.get(person_id).skills
            skills.append(Skill(
                name=person[12],
                experience=person[10]))

            new_person = Person(
                last_name=person[1],
                first_name=person[2],
                phone_number=person[7],
                company_name=person[16],
                age=person[3],
                skills=skills,
            )

            dict_person[person_id] = new_person

        return dict_person
