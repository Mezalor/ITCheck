import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
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
tk.Label(tkf_results, text=conf.session.get_number_tests(),
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


# Fenetre pop-up d'information sur les commandes / variable / exception
def info_command(test):
    tk_dialog = tk.Toplevel(tk_root)
    tk_dialog.title("Information Test")
    tk_dialog.geometry("500x300")

    tk.Label(tk_dialog, text="Information sur le test",
             font=("", 13, "bold")).pack(pady=10)

    tkt_info = tk.Text(tk_dialog, bg="white", height=5)
    tkt_info.insert("1.0", test.show_command())
    tkt_info.config(state="disable")
    tkt_info.pack(expand=True, fill="both", padx=5, pady=5)

    def copy_selection():
        tk_dialog.clipboard_clear()
        tk_dialog.clipboard_append(tkt_info.selection_get())

    def copy_all():
        tk_dialog.clipboard_clear()
        tk_dialog.clipboard_append(tkt_info.get("1.0", tk.END))

    tkf_button_select = tk.Frame(tk_dialog)
    tk.Button(tkf_button_select, text="Copier la sélection",
              command=copy_selection).pack(
                  side=tk.LEFT, padx=10)
    tk.Button(tkf_button_select, text="Tout copier",
              command=copy_all).pack(side=tk.LEFT, padx=10)

    tkf_button_select.pack(pady=10, padx=10)

    tk_dialog.wait_visibility()
    tk_dialog.grab_set()


def info_value(value):
    tk_dialog = tk.Toplevel(tk_root)
    tk_dialog.title("Information Valeur")
    tk_dialog.geometry("500x300")

    tk.Label(tk_dialog, text="Information sur la valeur",
             font=("", 13, "bold"), pady=10).pack()

    tkt_info = tk.Text(tk_dialog, bg="white", height=5)
    type_info = "Type : " + str(type(value)) + "\n"
    tkt_info.insert("1.0", type_info)
    value_info = "Valeur : " + str(value)
    tkt_info.insert("2.0", value_info)
    tkt_info.config(state="disable")
    tkt_info.pack(expand=True, fill="both", padx=5, pady=5)

    def copy_selection():
        tk_dialog.clipboard_clear()
        tk_dialog.clipboard_append(tkt_info.selection_get())

    def copy_all():
        tk_dialog.clipboard_clear()
        tk_dialog.clipboard_append(tkt_info.get("1.0", tk.END))

    tkf_button_select = tk.Frame(tk_dialog)
    tk.Button(tkf_button_select, text="Copier la sélection",
              command=copy_selection).pack(
                  side=tk.LEFT, padx=10)
    tk.Button(tkf_button_select, text="Tout copier",
              command=copy_all).pack(side=tk.LEFT, padx=10)

    tkf_button_select.pack(pady=10, padx=10)

    tk_dialog.wait_visibility()
    tk_dialog.grab_set()


def info_exception(err):
    tk_dialog = tk.Toplevel(tk_root)
    tk_dialog.title("Information erreur")
    tk_dialog.geometry("500x300")

    tk.Label(tk_dialog, text="Information sur l'erreur",
             font=("", 13, "bold"), pady=10).pack()

    infos_exception = ''.join(traceback.format_exception(
        etype=type(err), value=err, tb=err.__traceback__, limit=0))

    tkt_info = tk.Text(tk_dialog, bg="white", height=5)
    tkt_info.insert("1.0", infos_exception)
    tkt_info.config(state="disable")
    tkt_info.pack(expand=True, fill="both", padx=5, pady=5)

    def copy_selection():
        tk_dialog.clipboard_clear()
        tk_dialog.clipboard_append(tkt_info.selection_get())

    def copy_all():
        tk_dialog.clipboard_clear()
        tk_dialog.clipboard_append(tkt_info.get("1.0", tk.END))

    tkf_button_select = tk.Frame(tk_dialog)
    tk.Button(tkf_button_select, text="Copier la sélection",
              command=copy_selection).pack(
                  side=tk.LEFT, padx=10)
    tk.Button(tkf_button_select, text="Tout copier",
              command=copy_all).pack(side=tk.LEFT, padx=10)

    tkf_button_select.pack(pady=10, padx=10)

    tk_dialog.wait_visibility()
    tk_dialog.grab_set()


def show_tests(question_id):
    """ Affichage du tableau des tests """
    global tkf_test_table

    for widget in tkf_test_table.winfo_children():
        widget.destroy()

    tk.Label(tkf_test_table, text="N°").grid(column=0, row=0)
    tk.Label(tkf_test_table, text="Test").grid(column=1, row=0)
    tk.Label(tkf_test_table, text="Résultat attendu").grid(column=2, row=0)
    tk.Label(tkf_test_table, text="Résultat obtenu").grid(column=3, row=0)

    question = conf.session.get_question_byid(question_id)

    for test_id in range(question.get_number_tests()):
        test = question.get_test_byid(test_id)

        if not conf.work.is_answered(question_id):
            test_color = "#DADADA"
        elif conf.work.is_test_success(question_id, test_id):
            test_color = "green"
        elif test.get_level() == "warning":
            test_color = "yellow"
        else:
            test_color = "red"

        # Numéro du test
        s = tk.StringVar(tkf_test_table, value=str(test_id+1))
        tk.Entry(tkf_test_table, textvariable=s, justify="center", width=2,
                 state=tk.DISABLED).grid(column=0, row=test_id+1, sticky='ew')

        # Commande du test
        s = tk.StringVar(tkf_test_table)
        tke_command_test = tk.Entry(tkf_test_table, textvariable=s)
        tke_command_test.grid(column=1, row=test_id+1, sticky='ew')

        if test.get_hidden() == 0:
            s.set(test.show_command())
            tke_command_test.config(
                state="readonly", readonlybackground=test_color,
                font=("Consolas", 10, ""), cursor="hand2")
            tke_command_test.bind("<Button-1>",
                                  lambda e, test=test: info_command(test))
        else:
            s.set("caché")
            tke_command_test.config(
                state="disabled", disabledbackground=test_color,
                cursor="top_left_arrow", justify="center")

        # Résultat attendu du test
        result = conf.work.get_expected_result(question_id, test_id)

        s = tk.StringVar(tkf_test_table)
        tke_ex_result = tk.Entry(tkf_test_table, textvariable=s)
        tke_ex_result.grid(column=2, row=test_id+1, sticky='ew')

        if test.get_hidden() <= 1:
            s.set(result)
            tke_ex_result.config(
                state="readonly", readonlybackground=test_color,
                font=("Consolas", 10, ""), cursor="hand2")
            v = conf.work.get_expected_result_value(question_id, test_id)
            if isinstance(v, Exception):
                tke_ex_result.bind("<Button-1>",
                                   lambda e, v=v: info_exception(v))
                tke_ex_result.config(readonlybackground="red")
            else:
                tke_ex_result.bind("<Button-1>",
                                   lambda e, v=v: info_value(v))
        else:
            s.set("caché")
            tke_ex_result.config(
                state="disabled", disabledbackground=test_color,
                cursor="top_left_arrow", justify="center")

        # Résultat attendu du test
        s = tk.StringVar(tkf_test_table)
        tke_ob_result = tk.Entry(tkf_test_table, textvariable=s)
        tke_ob_result.grid(column=3, row=test_id+1, sticky='ew')

        if conf.work.is_answered(question_id):
            s.set(conf.work.get_obtained_result(question_id, test_id))
            tke_ob_result.config(
                state="readonly", readonlybackground=test_color,
                font=("Consolas", 10, ""), cursor="hand2")
            v = conf.work.get_obtained_result_value(question_id, test_id)
            if isinstance(v, Exception):
                tke_ob_result.bind("<Button-1>",
                                   lambda e, v=v: info_exception(v))
            else:
                tke_ob_result.bind("<Button-1>",
                                   lambda e, v=v: info_value(v))
        else:
            tke_ob_result.config(
                state="disabled", disabledbackground=test_color,
                cursor="top_left_arrow")
            tke_ob_result.unbind("<Button-1>")


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
        tke_status_import.config(state="normal", cursor="top_left_arrow")
        tke_status_import.delete(0, "end")
        tke_status_import.insert(0, "Pas d'erreur d'exécution")
        tke_status_import.config(readonlybackground="green", state="readonly")
        tke_status_import.unbind("<Button-1>")
    finally:
        update_view()


def check_all():
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


def goto_last_question():
    if question_focus_id > 0:
        goto_question(question_focus_id-1)


tkb_last_question.config(command=goto_last_question)


def goto_next_question():
    if question_focus_id < conf.session.get_number_questions()-1:
        goto_question(question_focus_id+1)


tkb_next_question.config(command=goto_next_question)


def check_question():
    import_work()
    conf.work.execute_tests_question(question_focus_id)
    conf.work.calculate_points_question(question_focus_id)

    update_view()


tkb_check_question.config(command=check_question)

tk_root.mainloop()
