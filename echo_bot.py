import telebot
from CandidatesRequestHandler import CandidatesRequestHandler, Skill

token = "1626590435:AAEEgKNn0Jturhx4HjBC6iK4ayGkS-2557I"
bot = telebot.TeleBot(token, parse_mode=None)

find_command = "find"
add_skill = "addskill"
set_skill_name = "setskillname"
remove_skill = "removeskill"
set_experience = "setminexperience"
remove_experience = "removeskillexperience"
set_gender = "setgender"
remove_gender = "removegender"
set_employed_status = "setemployedstatus"
remove_employed_status = "removeemployedstatus"
set_higher_education = "sethashigheredu"
remove_higher_education = "removehighereducation"
set_age_range = "setagerange"
remove_age_range = "removeagerange"
help = "help"
show = "show"

age_range = None
is_employed = None
hasHigherEducation = None
gender = None
skills_list: [Skill] = []
find_triggered = True

last_skill = None


@bot.message_handler(commands=["start"])
def on_start(message):
    bot.send_message(message.chat.id, "Welcome, here commands to use")
    on_help(message)


@bot.message_handler(commands=[help])
def on_help(message):
    chat_id = message.chat.id

    help_msg = f"/{find_command} to find employee by selected criteria\n" + \
               f"/{show} to show all requirements\n" + \
               f"/{add_skill} to add skill\n" + \
               f"/{add_skill} to add skill\n" + \
               f"/{set_skill_name}+ name to select skill name\n" + \
               f"/{set_experience}+ number representing minimum experience\n" + \
               f"/{set_gender} + female or male to select required genders\n" + \
               f"/{remove_gender} to remove any gender requirements\n" + \
               f"/{set_higher_education}+ true or false to select only one education option\n" + \
               f"/{remove_higher_education} to remove any education requirements\n" + \
               f"/{set_employed_status}+ true or false to select required employment status\n" + \
               f"/{remove_employed_status} to remove any employment status requirements\n"

    bot.send_message(chat_id, help_msg)


def clear_after_find():
    global age_range, is_employed, hasHigherEducation, gender, skills_list, find_triggered
    if find_triggered:
        age_range = None
        is_employed = None
        hasHigherEducation = None
        gender = None
        skills_list = []
        find_triggered = False


def send_unknown_params(message):
    bot.send_message(message.chat.id, "invalid params. Use /help to see commands")


@bot.message_handler(commands=[show])
def show_req(message):
    chat_id = message.chat.id
    msg = ""

    if age_range is not None:
        msg += f"age range from {age_range.start} to {age_range.stop} \n"
    if is_employed is not None:
        msg += f"is employed {is_employed} \n"
    if hasHigherEducation is not None:
        msg += f"is employed {hasHigherEducation} \n"
    if gender is not None:
        gender_name = "female" if gender == 1 else "male"
        msg += f"is employed {hasHigherEducation} \n"

    for skill in skills_list:
        msg += str(skill)

    bot.send_message(chat_id, msg)


@bot.message_handler(commands=[remove_skill])
def on_remove_skill(message):
    global skills_list
    words = message.text.split()

    if len(words) == 1 and len(skills_list) > 0:
        skills_list = skills_list[1:]
        return

    try:
        index = int(words[1]) - 1
        skills_list = skills_list[:index] + skills_list[index + 1:]
    except:
        send_unknown_params(message)


@bot.message_handler(commands=[set_skill_name])
def on_set_skillname(message):
    chat_id = message.chat.id
    name = message.text[len(set_skill_name) + 1:].strip()
    global last_skill
    if name is None:
        return

    if last_skill is None:
        last_skill = Skill(name)
        return
    else:
        last_skill.name = name


@bot.message_handler(commands=[set_experience])
def on_set_experience(message):
    clear_after_find()
    chat_id = message.chat.id
    global last_skill
    if last_skill is None:
        bot.send_message(chat_id, "No skill where to set experience")
        return
    words = message.text.split()

    try:
        last_skill.experience = int(words[1])
    except:
        send_unknown_params(message)


@bot.message_handler(commands=[remove_experience])
def on_remove_experience(message):
    clear_after_find()

    global last_skill
    if last_skill is not None:
        last_skill.experience = None


@bot.message_handler(commands=[add_skill])
def on_add_skill(message):
    clear_after_find()
    chat_id = message.chat.id
    global last_skill, skills_list
    if last_skill is None:
        bot.send_message(chat_id, "No skill to add")
        return

    skills_list = [last_skill] + skills_list
    last_skill = None


@bot.message_handler(commands=[set_age_range])
def on_set_age_range(message):
    clear_after_find()
    global age_range
    words = message.text.split()

    try:
        age_start = int(words[1])
    except:
        send_unknown_params(message)
        return

    try:
        age_end = int(words[2])
    except:
        send_unknown_params(message)
        return

    age_range = range(age_start, age_end + 1)


@bot.message_handler(commands=[remove_age_range])
def on_remove_age_range(message):
    clear_after_find()
    global age_range
    age_range = None


@bot.message_handler(commands=[set_employed_status])
def on_set_employed_status(message):
    clear_after_find()
    global is_employed
    words = message.text.split()

    if len(words) > 1:
        if words[1] == "true":
            is_employed = True
        elif words[1] == "false":
            is_employed = False
        else:
            send_unknown_params(message)


@bot.message_handler(commands=[remove_employed_status])
def on_remove_employed_status(message):
    clear_after_find()
    global is_employed
    is_employed = None


@bot.message_handler(commands=[set_higher_education])
def on_set_higher_edu(message):
    clear_after_find()
    global hasHigherEducation
    words = message.text.split()

    if len(words) > 1:
        if words[1] == "true":
            hasHigherEducation = True
        elif words[1] == "false":
            hasHigherEducation = False
        else:
            send_unknown_params(message)


@bot.message_handler(commands=[remove_higher_education])
def on_remove_higher_edu(message):
    clear_after_find()
    global hasHigherEducation
    hasHigherEducation = None


@bot.message_handler(commands=[set_gender])
def on_set_gender(message):
    clear_after_find()
    global gender
    words = message.text.split()
    if len(words) > 1:
        if words[1] == "female":
            gender = 1
        elif words[1] == "male":
            gender = 0
        else:
            send_unknown_params(message)


@bot.message_handler(commands=[remove_gender])
def on_set_gender(message):
    clear_after_find()
    global gender
    gender = None


@bot.message_handler(commands=[find_command])
def on_find(message):
    global find_triggered
    find_triggered = True
    page_size = 1
    page_index = 1
    try:
        page_size = int(message.text.split()[1])
    except:
        pass

    try:
        page_index = int(message.text.split()[2])
    except:
        pass

    if page_size > 5: page_size = 5
    emp = find_employee()

    for i, employee in enumerate(emp):
        if i < page_size * page_index and i >= page_size * (page_index - 1):
            bot.send_message(message.chat.id, employee)


def find_employee():
    suitable_candidates = CandidatesRequestHandler.get_candidates(
        age_range=age_range,
        gender=gender,
        required_skills=skills_list,
        is_currently_employed=is_employed,
        has_higher_education=hasHigherEducation,
    )

    suitable_employee_list = []

    for cand in suitable_candidates:
        suitable_employee_list.append([
            f"{cand.first_name} {cand.last_name} "
            f"{cand.phone_number} "
            f"{cand.skills} age:{cand.age} "
            f"{cand.company_name}"])

    return suitable_employee_list


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text)
    # bot.reply_to(message, message.text)


def start():
    bot.polling(none_stop=True)
