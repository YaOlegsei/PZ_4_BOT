from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from CandidatesRequestHandler import Skill
from CandidatesRequestHandler import CandidatesRequestHandler


def display_full_name():
    messagebox.showinfo("GUI Python", "Eboi" + " " + "A sho haipovo")


gender_options = ("any gender", "male", "female")

employed_options = ["any employed status", "employed", "unemployed"]

higher_education_options = ["any education", "has higher education", "Doesn't have higher education"]

root = Tk()
root.title("Экспертная система поиска сотрудников")

skills_requirements_list_box = Listbox()
skills_requirements_list_box \
    .grid(row=6, column=0, columnspan=2, sticky=W + E, padx=5, pady=5)


suitable_employee_list = Listbox()
suitable_employee_list \
    .grid(row=8, column=0, columnspan=4, sticky=W + E, padx=5, pady=5)

foundLable = Label(text="")
foundLable.grid(row=7, column=1, columnspan=2, sticky=W + E, padx=5, pady=5)


def delete_skill():
    selection = skills_requirements_list_box.curselection()
    if len(selection) <= 0: return
    skills_requirements_list_box.delete(selection[0])
    del skills_list[selection[0]]


skills_list = []


def add_skill():
    if not skill_name.get() or skill_experience.get() < 0: return
    new_skill = Skill(
        experience=skill_experience.get(),
        name=skill_name.get(),
    )
    skills_list.insert(0, new_skill)
    skills_requirements_list_box.insert(0, new_skill)


def create_combobox(list, row, string_var):
    combobox = ttk.Combobox(
        root,
        width=27,
        textvariable=string_var)
    combobox['state'] = 'readonly'
    combobox['values'] = list
    combobox.grid(row=row, column=0, sticky="w")

    combobox.current(0)
    return combobox


should_check_age = BooleanVar()
should_check_age.set(False)
skill_name = StringVar()
skill_experience = IntVar()
age_from = IntVar()
age_until = IntVar()
age_until.set(100)
genderVar = StringVar()
employedVar = StringVar()
higher_education_var = StringVar()


def start():
    create_combobox(gender_options, 0, genderVar)

    create_combobox(employed_options, 1, employedVar)

    create_combobox(higher_education_options, 2, higher_education_var)

    skill_label = Label(text="Введите название навыка:")
    skill_experience_label = Label(text="требуемый опыт навыка:")

    skill_label.grid(row=3, column=0, sticky="w")

    c1 = Checkbutton(root, text="Should filter by age?",
                     variable=should_check_age,
                     onvalue=1, offvalue=0,
                     )
    c1.grid(row=5, sticky="w", column=0, padx=5, pady=5)

    skill_name_entry = Entry(textvariable=skill_name)
    skill_experience_entry = Entry(textvariable=skill_experience)
    age_from_entry = Entry(textvariable=age_from)
    age_until_entry = Entry(textvariable=age_until)

    Label(text="Enter age from").grid(row=5, column=1, padx=5, pady=5)
    Label(text="until").grid(row=5, column=3, padx=5, pady=5)
    age_from_entry.grid(row=5, column=2, padx=5, pady=5)
    age_until_entry.grid(row=5, column=4, padx=5, pady=5)
    skill_name_entry.grid(row=3, column=1, padx=5, pady=5)
    skill_experience_entry.grid(row=4, column=1, padx=5, pady=5)

    add_skill_req_button = Button(text="Add skill requirements", command=add_skill)
    add_skill_req_button.grid(row=4, column=2, padx=5, pady=5, sticky="w")

    add_skill_req_button = Button(text="Delete skill requirements", command=delete_skill)
    add_skill_req_button.grid(row=4, column=3, padx=5, pady=5, sticky="w")

    find_employees = Button(text="Find employee", command=find_employee)
    find_employees.grid(row=4, column=4, padx=5, pady=5, sticky="w")

    root.mainloop()


def find_employee():
    selected_gender_option = genderVar.get()
    selected_higher_education_option = higher_education_var.get()
    selected_employed_status = employedVar.get()
    gender = None
    if selected_gender_option == gender_options[1]:
        gender = 0
    elif selected_gender_option == gender_options[2]:
        gender = 1

    hasHigherEducation = None

    if selected_higher_education_option == higher_education_options[1]:
        hasHigherEducation = True
    elif selected_higher_education_option == higher_education_options[2]:
        hasHigherEducation = False

    is_employed = None

    if selected_employed_status == employed_options[1]:
        is_employed = True
    elif selected_employed_status == employed_options[2]:
        is_employed = False

    age_range = None

    if should_check_age.get():
        from_age = 0
        try:
            from_age = age_from.get()
        except:
            pass
        until_age = 100
        try:
            until_age = age_until.get()
        except:
            pass
        age_range = range(from_age, until_age)

    suitable_candidates = CandidatesRequestHandler.get_candidates(
        age_range=age_range,
        gender=gender,
        required_skills=skills_list,
        is_currently_employed=is_employed,
        has_higher_education=hasHigherEducation,
    )

    suitable_employee_list.delete(0, 'end')
    foundLable['text'] = f"Found {len(suitable_candidates)} employees"
    for cand in suitable_candidates:
        suitable_employee_list.insert(0,
                                      f"{cand.first_name} {cand.last_name} "
                                      f"{cand.phone_number} "
                                      f"{cand.skills} age:{cand.age} "
                                      f"{cand.company_name}")
