import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from tkinter import font
import traceback

import config as conf

# Propriétés de la fenêtre principale
tk_root = tk.Tk()
tk_root.title("ITCheck")
tk_root.geometry("800x710")

# Titre du TP
tk.Label(tk_root, text=conf.session.name,
         font=("", 15, "bold"), pady=10).pack()

# Partie importation du fichier source python
tkf_import = tk.Frame(tk_root, pady=10)

tk.Label(tkf_import, text="Fichier source", padx=10).pack(side=tk.LEFT)
tke_file_loc = tk.Entry(tkf_import, background="white")
tke_file_loc.pack(side=tk.LEFT, fill="both", expand=True)
tkb_search = tk.Button(tkf_import, text="Parcourir")
tkb_search.pack(side=tk.LEFT)
tkb_check_all = tk.Button(tkf_import, text="Évaluer")
tkb_check_all.pack(side=tk.LEFT, padx=(15, 5))

tkf_import.pack(fill="x")

# Bandeau indiquant si le fichier s'est exécuté correctement
tke_status_import = tk.Entry(tk_root, state="readonly",
                             justify="center", cursor="top_left_arrow")
tke_status_import.pack(fill="x", padx=10)

# Encadré des résultats : Notes, questions réussies et tests passés
tkf_results = tk.LabelFrame(tk_root, padx=15, pady=15)

tk.Label(tkf_results, text="Note :",
         font=("", 12, "bold")).grid(column=0, row=0, sticky="e", padx=5)
tks_mark = tk.StringVar(tkf_results, value="0.0")
tk.Label(tkf_results, textvariable=tks_mark,
         font=("", 12, "bold")).grid(column=1, row=0, sticky="e", padx=5)
tk.Label(tkf_results, text="/",
         font=("", 12, "bold")).grid(column=2, row=0)
tk.Label(tkf_results, text=conf.session.get_total_scale(),
         font=("", 12, "bold")).grid(column=3, row=0, sticky="w", padx=5)

tk.Label(tkf_results, text="Questions :",
         font=("", 12, "bold")).grid(column=0, row=1, sticky="e", padx=5)
tks_success_questions = tk.StringVar(tkf_results, value="0")
tk.Label(tkf_results, textvariable=tks_success_questions,
         font=("", 12, "bold")).grid(column=1, row=1, sticky="e", padx=5)
tk.Label(tkf_results, text="/",
         font=("", 12, "bold")).grid(column=2, row=1)
tk.Label(tkf_results, text=conf.session.get_number_questions(),
         font=("", 12, "bold")).grid(column=3, row=1, sticky="w", padx=5)

tk.Label(tkf_results, text="Tests :",
         font=("", 12, "bold")).grid(column=0, row=2, sticky="e", padx=5)
tks_success_tests = tk.StringVar(tkf_results, value="0")
tk.Label(tkf_results, textvariable=tks_success_tests,
         font=("", 12, "bold")).grid(column=1, row=2, sticky="e", padx=5)
tk.Label(tkf_results, text="/",
         font=("", 12, "bold")).grid(column=2, row=2)
tk.Label(tkf_results, text=conf.session.get_number_tests_without_info(),
         font=("", 12, "bold")).grid(column=3, row=2, sticky="w", padx=5)

tkf_results.pack(pady=15)

# Résultat des tests par question
tk.Label(tk_root, text="Résultat des tests par question",
         font=("", 10, "bold"), pady=5).pack()

# Bandeau des résultats par question permettant de sélectionner une question
tkf_questions = tk.Frame(tk_root)

tkb_questions = []
pixelVirtual = tk.PhotoImage()
for i in range(conf.session.get_number_questions()):
    tkb_questions.append(tk.Button(tkf_questions, image=pixelVirtual,
                                   height=15, width=15))
    if i == 0:
        tkb_questions[-1].config(state=tk.DISABLED, relief=tk.SUNKEN)
    tkb_questions[-1].pack(side=tk.LEFT)

tkf_questions.pack()

# Bandeau nom de la question et bouton suivant/précédent
tkf_question_title = tk.Frame(tk_root)
question_focus_id = 0

tkb_last_question = tk.Button(tkf_question_title, text="<", state=tk.DISABLED)
tkb_last_question.pack(side=tk.LEFT)
qu_name = conf.session.get_question_byid(question_focus_id).get_name()
tks_name_question = tk.StringVar(tkf_question_title,
                                 value=qu_name)
tk.Label(tkf_question_title, textvariable=tks_name_question,
         font=("", 12, "bold"), width=30).pack(side=tk.LEFT)
tkb_next_question = tk.Button(tkf_question_title, text=">")
tkb_next_question.pack(side=tk.LEFT)

tkf_question_title.pack(pady=10)

# Information sur la question : fonction/varaible à tester et note obtenue
tkf_question_info = tk.Frame(tk_root)

tk.Label(tkf_question_info, text="Note : ").grid(column=0, row=0, sticky="e")
qu_mark = "0.0 / "
qu_mark += str(conf.session.get_question_byid(question_focus_id).get_scale())
tks_mark_question = tk.StringVar(tkf_question_info, value=qu_mark)
tk.Label(tkf_question_info, textvariable=tks_mark_question,
         font=("", 10, "bold")).grid(column=1, row=0, sticky="w")

tk.Label(tkf_question_info,
         text="Fonction/Variable à tester : ").grid(column=0, row=1,
                                                    sticky="e")
qu_func = conf.session.get_question_byid(question_focus_id).get_func_name()
tks_func_name = tk.StringVar(tkf_question_info, value=qu_func)
ttk.Style().configure('pad.TEntry', padding='5 1 1 1')
ttk.Entry(tkf_question_info, textvariable=tks_func_name, state="readonly",
          style="pad.TEntry", font=("Consolas", 10, "bold"),
          width=25).grid(column=1, row=1, sticky="w")

tkb_check_question = tk.Button(tkf_question_info, text="Évaluer la question")
tkb_check_question.grid(column=0, row=2, columnspan=2, pady=10)

tkf_question_info.pack()

# Tableau listant les résultats des tests
tkf_test_table = tk.Frame(tk_root)

tk.Label(tkf_test_table, text="N°").grid(column=0, row=0)
tk.Label(tkf_test_table, text="Test").grid(column=1, row=0)
tk.Label(tkf_test_table, text="Résultat attendu").grid(column=2, row=0)
tk.Label(tkf_test_table, text="Résultat obtenu").grid(column=3, row=0)

max_t = conf.session.get_max_numer_tests()
# Liste des numéros des tests
tks_nbt = [None for _ in range(max_t)]
tke_nbt = [None for _ in range(max_t)]
# Liste des commande du test
tks_ct = [None for _ in range(max_t)]
tke_ct = [None for _ in range(max_t)]
# Liste des resultats attendus du test
tks_ex = [None for _ in range(max_t)]
tke_ex = [None for _ in range(max_t)]
# Liste des resultats obtenus du test
tks_ob = [None for _ in range(max_t)]
tke_ob = [None for _ in range(max_t)]

for test_id in range(max_t):
    # Numéro du test
    tks_nbt[test_id] = tk.StringVar(tkf_test_table, value=str(test_id+1))
    tke_nbt[test_id] = tk.Entry(tkf_test_table, textvariable=tks_nbt[test_id],
                                justify="center", width=2, state=tk.DISABLED)
    tke_nbt[test_id].grid(column=0, row=test_id+1, sticky='ew')

    # Commande du test
    tks_ct[test_id] = tk.StringVar(tkf_test_table)
    tke_ct[test_id] = tk.Entry(tkf_test_table, textvariable=tks_ct[test_id])
    tke_ct[test_id].grid(column=1, row=test_id+1, sticky='ew')

    # Résultat attendu du test
    tks_ex[test_id] = tk.StringVar(tkf_test_table)
    tke_ex[test_id] = tk.Entry(tkf_test_table, textvariable=tks_ex[test_id])
    tke_ex[test_id].grid(column=2, row=test_id+1, sticky='ew')

    # Résultat obtenu du test
    tks_ob[test_id] = tk.StringVar(tkf_test_table)
    tke_ob[test_id] = tk.Entry(tkf_test_table, textvariable=tks_ob[test_id])
    tke_ob[test_id].grid(column=3, row=test_id+1, sticky='ew')


# Fenetre pop-up d'information sur les commandes / variable / exception
def info_popup(info_type, data, stdout=""):
    title = {"com": "Information sur le test",
             "val": "Information sur la valeur",
             "err": "Information sur l'erreur",
             "std": "Affichage de la sortie (stdout)"}

    tk_dialog = tk.Toplevel(tk_root)
    tk_dialog.geometry("600x300")

    tks_popup_title = tk.StringVar(tk_dialog, value=title[info_type])
    tk.Label(tk_dialog, textvariable=tks_popup_title,
             font=("", 13, "bold")).pack(pady=10)

    tkt_info = tk.Text(tk_dialog, bg="white", height=5)
    if info_type == "com":
        tkt_info.insert("1.0", data.show_command())
    elif info_type == "val":
        type_info = "Type : " + str(type(data)) + "\n"
        tkt_info.insert("1.0", type_info)
        value_info = "Valeur : " + str(data)
        tkt_info.insert("2.0", value_info)
    elif info_type == "err":
        try:
            infos_exception = ''.join(traceback.format_exception(
                etype=type(data), value=data, tb=data.__traceback__, limit=0))
        except TypeError:
            infos_exception = ''.join(traceback.format_exception(data,
                                                                 limit=0))
        tkt_info.insert("1.0", infos_exception)
    elif info_type == "std":
        tkt_info.insert("1.0", data)

    tkt_info.config(state="disable")
    tkt_info.pack(expand=True, fill="both", padx=5, pady=5)

    def copy_selection():
        tk_dialog.clipboard_clear()
        tk_dialog.clipboard_append(tkt_info.selection_get())
        tk_dialog.update()

    def copy_all():
        tk_dialog.clipboard_clear()
        tk_dialog.clipboard_append(tkt_info.get("1.0", tk.END))
        tk_dialog.update()

    tkf_button_select = tk.Frame(tk_dialog)
    tk.Button(tkf_button_select, text="Copier la sélection",
              command=copy_selection).pack(
                  side=tk.LEFT, padx=10)
    tk.Button(tkf_button_select, text="Tout copier",
              command=copy_all).pack(side=tk.LEFT, padx=10)

    def switch_display():
        if tks_popup_title.get() == title["val"]:
            tks_popup_title.set(title["std"])
            tkt_info.config(state="normal")
            tkt_info.delete(1.0, tk.END)
            tkt_info.insert("1.0", stdout)
            tkt_info.config(state="disable")
            tks_display.set("Affichage de la valeur")

        elif tks_popup_title.get() == title["std"]:
            tks_popup_title.set(title["val"])
            tkt_info.config(state="normal")
            tkt_info.delete(1.0, tk.END)
            type_info = "Type : " + str(type(data)) + "\n"
            tkt_info.insert("1.0", type_info)
            value_info = "Valeur : " + str(data)
            tkt_info.insert("2.0", value_info)
            tkt_info.config(state="disable")
            tks_display.set("Affichage de la sortie (stdout)")

    if info_type == "val" and stdout != "":
        tks_display = tk.StringVar(tkf_button_select)
        tkb_display = tk.Button(tkf_button_select, textvariable=tks_display,
                                command=switch_display)
        tkb_display.pack(side=tk.LEFT, padx=10)
        tks_display.set("Affichage de la sortie (stdout)")

    tkf_button_select.pack(pady=10, padx=10)

    tk_dialog.wait_visibility()
    tk_dialog.grab_set()


def info_command(test):
    info_popup("com", test)


def info_value(value):
    if isinstance(value, tuple):
        info_popup("val", value[0], value[1])
    else:
        info_popup("val", value)


def info_exception(err):
    info_popup("err", err)


def info_std(std):
    info_popup("std", std)


def show_tests(question_id):
    """ Affichage du tableau des tests """
    question = conf.session.get_question_byid(question_id)

    for test_id in range(question.get_number_tests()):
        tke_nbt[test_id].grid()
        tke_ct[test_id].grid()
        tke_ex[test_id].grid()
        tke_ob[test_id].grid()

        test = question.get_test_byid(test_id)

        if not conf.work.get_enabled_result(question_id, test_id):
            test_color = "#DADADA"
        elif test.get_level() == "info":
            test_color = "#AFFFFA"
        elif conf.work.is_test_success(question_id, test_id):
            if conf.work.get_std_result(question_id, test_id) != "":
                test_color = "#86FF86"
            else:
                test_color = "green"
        elif conf.work.is_test_fail_type(question_id, test_id):
            test_color = "yellow"
        else:
            test_color = "red"

        # Commande du test
        if test.get_hidden() == 0:
            tks_ct[test_id].set(test.show_command())
            tke_ct[test_id].config(
                state="readonly", readonlybackground=test_color,
                font=("Consolas", 10, ""), cursor="hand2", justify="left")
            tke_ct[test_id].bind("<Button-1>",
                                 lambda e, test=test: info_command(test))
        else:
            tks_ct[test_id].set("caché")
            tke_ct[test_id].config(
                state="disabled", disabledbackground=test_color,
                font=font.nametofont("TkDefaultFont"),
                cursor="top_left_arrow", justify="center")
            tke_ct[test_id].unbind("<Button-1>")

        # Résultat attendu du test
        result = conf.work.get_expected_result(question_id, test_id)

        if test.get_level() == "info":
            tks_ex[test_id].set("test hors barème pour information")
            tke_ex[test_id].config(
                state="disabled", disabledbackground=test_color,
                font=font.nametofont("TkDefaultFont"),
                cursor="top_left_arrow", justify="center")
            tke_ex[test_id].unbind("<Button-1>")
        elif test.get_hidden() <= 1:
            tks_ex[test_id].set(result)
            tke_ex[test_id].config(
                state="readonly", readonlybackground=test_color,
                font=("Consolas", 10, ""), cursor="hand2", justify="left")
            v = conf.work.get_expected_result_value(question_id, test_id)
            if isinstance(v, Exception):
                tke_ex[test_id].bind("<Button-1>",
                                     lambda e, v=v: info_exception(v))
                tke_ex[test_id].config(readonlybackground="red")
            else:
                tke_ex[test_id].bind("<Button-1>",
                                     lambda e, v=v: info_value(v))
        else:
            tks_ex[test_id].set("caché")
            tke_ex[test_id].config(
                state="disabled", disabledbackground=test_color,
                font=font.nametofont("TkDefaultFont"),
                cursor="top_left_arrow", justify="center")
            tke_ex[test_id].unbind("<Button-1>")

        # Résultat obtenu du test
        if conf.work.get_enabled_result(question_id, test_id):
            tks_ob[test_id].set(conf.work.get_obtained_result(question_id,
                                                              test_id))
            tke_ob[test_id].config(
                state="readonly", readonlybackground=test_color,
                font=("Consolas", 10, ""), cursor="hand2")
            v = conf.work.get_obtained_result_value(question_id, test_id)
            if isinstance(v, Exception):
                tke_ob[test_id].bind("<Button-1>",
                                     lambda e, v=v: info_exception(v))
            else:
                std = conf.work.get_std_result(question_id, test_id)
                v = v, std
                tke_ob[test_id].bind("<Button-1>",
                                     lambda e, v=v: info_value(v))
        else:
            tks_ob[test_id].set("")
            tke_ob[test_id].config(
                state="disabled", disabledbackground=test_color,
                font=font.nametofont("TkDefaultFont"),
                cursor="top_left_arrow")
            tke_ob[test_id].unbind("<Button-1>")

    for test_id in range(question.get_number_tests(), max_t):
        tke_nbt[test_id].grid_remove()
        tke_ct[test_id].grid_remove()
        tke_ex[test_id].grid_remove()
        tke_ob[test_id].grid_remove()


show_tests(question_focus_id)

tkf_test_table.grid_columnconfigure(0, weight=2)
tkf_test_table.grid_columnconfigure(1, weight=40)
tkf_test_table.grid_columnconfigure(2, weight=30)
tkf_test_table.grid_columnconfigure(3, weight=30)
tkf_test_table.pack(fill="x")


def select_work_filename():
    filename = fd.askopenfilename(title="Ouvrir un TP python",
                                  filetypes=[("Fichier Python", "*.py"),
                                             ("Tous les fichiers", "*")])
    if filename != "":
        tke_file_loc.delete(0, "end")
        tke_file_loc.insert(0, filename)


tkb_search.config(command=select_work_filename)


def update_view():
    mark = int(100*conf.work.get_total_mark())/100
    tks_mark.set(mark)

    nb_passed_questions = conf.work.get_total_passed_questions()
    tks_success_questions.set(nb_passed_questions)

    nb_passed_tests = conf.work.get_total_passed_tests()
    tks_success_tests.set(nb_passed_tests)

    for i in range(len(tkb_questions)):
        tkb_questions[i].config(background=conf.work.get_question_color(i))

    qu_mark = str(int(100*conf.work.get_question_mark(question_focus_id))/100)
    qu_mark += " / "
    qu_mark += str(conf.session.get_question_byid(
        question_focus_id).get_scale())
    tks_mark_question.set(qu_mark)

    show_tests(question_focus_id)


def import_work():
    try:
        conf.work.import_module_work(tke_file_loc.get())
    except Exception as err:
        tke_status_import.config(state="normal", cursor="hand2")
        tke_status_import.delete(0, "end")
        tke_status_import.insert(0, "Erreur d'exécution : " + str(err))
        tke_status_import.config(readonlybackground="red", state="readonly")
        tke_status_import.bind("<Button-1>",
                               lambda e, err=err: info_exception(err))
    else:
        std = conf.work.get_stdout()
        if std == "":
            tke_status_import.config(state="normal", cursor="top_left_arrow")
            tke_status_import.delete(0, "end")
            tke_status_import.insert(0, "Pas d'erreur d'exécution")
            tke_status_import.config(readonlybackground="green",
                                     state="readonly")
            tke_status_import.unbind("<Button-1>")
        else:
            tke_status_import.config(state="normal", cursor="hand2")
            tke_status_import.delete(0, "end")
            tke_status_import.insert(0, "Pas d'erreur d'exécution. " +
                                        "Voir l'affichage (stdout)")
            tke_status_import.config(readonlybackground="#86FF86",
                                     state="readonly")
            tke_status_import.bind("<Button-1>",
                                   lambda e, std=std: info_std(std))
    finally:
        update_view()


def check_all():
    conf.work.clear_all()
    import_work()
    conf.work.execute_all_tests()
    conf.work.calculate_all_points()

    update_view()


tkb_check_all.config(command=check_all)


def goto_question(id):
    global question_focus_id

    tkb_questions[question_focus_id].config(state=tk.NORMAL, relief=tk.RAISED)
    tkb_questions[id].config(state=tk.DISABLED, relief=tk.SUNKEN)

    if id == 0:
        tkb_last_question.config(state=tk.DISABLED)
    else:
        tkb_last_question.config(state=tk.NORMAL)
    if id == conf.session.get_number_questions()-1:
        tkb_next_question.config(state=tk.DISABLED)
    else:
        tkb_next_question.config(state=tk.NORMAL)

    tks_name_question.set(conf.session.get_question_byid(id).get_name())

    qu_mark = str(int(100*conf.work.get_question_mark(id))/100)
    qu_mark += " / "
    qu_mark += str(conf.session.get_question_byid(id).get_scale())
    tks_mark_question.set(qu_mark)

    tks_func_name.set(conf.session.get_question_byid(id).get_func_name())

    show_tests(id)

    question_focus_id = id


for i in range(conf.session.get_number_questions()):
    tkb_questions[i].config(command=lambda i=i: goto_question(i))


def goto_last_question(ev=None):
    if question_focus_id > 0:
        goto_question(question_focus_id-1)


tkb_last_question.config(command=goto_last_question)
tk_root.bind('<Left>', goto_last_question)


def goto_next_question(ev=None):
    if question_focus_id < conf.session.get_number_questions()-1:
        goto_question(question_focus_id+1)


tkb_next_question.config(command=goto_next_question)
tk_root.bind('<Right>', goto_next_question)


def check_question():
    import_work()
    conf.work.execute_tests_question(question_focus_id)
    conf.work.calculate_points_question(question_focus_id)

    update_view()


tkb_check_question.config(command=check_question)

tk_root.mainloop()
