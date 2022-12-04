import PySimpleGUI as sg
import random as ran
import os
import sys

def main():
    sg.theme('DarkTeal2')

    PASTEL_RED = '#ff7a63'
    SKY_BLUE = '#00a6ff'
    PASTEL_DARK_GREEN = '#386c5f'
    # sg.theme_background_color(())
    category = ['GENERAL', 'PRIORITY', 'BANKING', 'SHOPPING', 'GAME', 'SPAM', 'MISC']
    user_type = ['EMAIL', 'USERNAME']
    password_length = [8, 9, 10, 11, 12, 13, 14, 15, 16]
    output = sg.Multiline(write_only=False, disabled=True, key='gen_pass', no_scrollbar=True)

    cat_combo = sg.Combo(category, default_value='PICK ONE', size = (12, 1), key='categories', readonly=True)

    ent_usertype = sg.Text('Enter username: ', visible=False, font=('Helvetica', 14))
    usertype_box = sg.InputText(visible=False, key='userlogin')

    title_input = sg.InputText(key='title')
    
    user_type_dropdown = sg.Combo(user_type, enable_events=True, default_value='PICK ONE', size = (12, 1), key='users_type', readonly=True)
    #for the folder path
    base_folder = str(os.path.expanduser('~\Documents'))
    def_fol_path = sg.InputText(default_text=base_folder, disabled=False, key='folder_path')
    browse_folder = sg.FolderBrowse('CHANGE',initial_folder=str(base_folder), key='chosen_folder')

    cb_pass_txt = sg.Text('Copied Password to Clipboard!', text_color = PASTEL_RED, justification='r',visible=False)
    lower = 'abcdefghijklmnopqrstuvwxyz'
    upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!@#$%^&*().'
    available_characters = lower# + upper + numbers + symbols

    # key returns a dict
    layout =    [[sg.Text('Folder Path:',font=('Helvetica', 14))],
                [def_fol_path, browse_folder],
                [sg.Text("Category: ",font=('Helvetica', 14)), sg.Push(), sg.Button('OPEN DIR', font=('Helvetica', 10))],
                [cat_combo],
                [sg.Text("User type:", font=('Helvetica', 14))],
                [user_type_dropdown],
                [ent_usertype],
                [usertype_box],
                [sg.Text(f'Title to remember point of interest:', font=('Helvetica', 14))],
                [title_input],
                [sg.Text(f'Length of password:', font=('Helvetica', 14))],
                [sg.Combo(password_length, default_value=12, key='length')],
                [sg.Text(f'Parameters:', font=('Helvetica', 14))],
                [sg.Checkbox('Capital letters', key='capitals'), sg.Checkbox('Symbols', key='symbols'), sg.Checkbox('Numbers', key='numbers')],
                [sg.Text('Generated Password:',font=('Helvetica', 14)), cb_pass_txt],
                [output],
                [sg.Button('GENERATE', font=('Helvetica', 12)), sg.Button('SAVE', font=('Helvetica', 12), button_color=PASTEL_DARK_GREEN), sg.Push(), sg.Button('CLEAR', font=('Helvetica', 12), button_color=SKY_BLUE), sg.Button('EXIT', font=('Helvetica',  12), button_color=PASTEL_RED)]]

    # Create the window
    cwd = str(os.getcwd())
    window = sg.Window("Password Generator", layout, icon=str(os.path.join(cwd, 'pwdgen_icon.ico')))

    # Create an event loop
    while True:
        event, values = window.read()

        # reset to just lower
        available_characters = lower

        if event == 'EXIT' or event == sg.WIN_CLOSED:
            break

        if values['users_type'] == 'PICK ONE':
            pass
        elif values['users_type'] == 'EMAIL':
            ent_usertype.update('Enter email:',visible=True, font=('Helvetica', 14))
            usertype_box.update(visible=True)
        elif values['users_type'] == 'USERNAME':
            ent_usertype.update('Enter username:',visible=True)
            usertype_box.update(visible=True)

        if event == 'GENERATE':
            if (values['categories'] != 'PICK ONE' and
                values['users_type'] != 'PICK ONE' and 
                values['title'] != '' and
                values['userlogin'] != ''):

                # checks if checkbox is marked, if so, add to pool of available characters
                if values['capitals'] == True:
                    available_characters += upper
                if values['symbols'] == True:
                    available_characters += symbols
                if values['numbers'] == True:
                    available_characters += numbers
                
                password = ''.join(ran.sample(available_characters, values['length']))
                output.update(password)
                cb_pass = password
            else:
                output.update('Missing a required value.')

        if event == 'SAVE':
            if(values['gen_pass'] == '' or values['gen_pass'] == 'Missing a required value.'):
                cb_pass_txt.update('Nothing to save!', visible=True)
            else:
                sg.clipboard_set(cb_pass)
                cb_pass_txt.update('Copied Password to Clipboard!', visible=True)

                if values['chosen_folder'] == '':
                    actual_path = str(base_folder)
                    mkd_path = os.path.join(actual_path, 'PWD GEN', values['categories'])

                    if not os.path.exists(mkd_path):
                        os.makedirs(f"{mkd_path}")
                    with open(f"{mkd_path}/{values['title']}.txt", mode = "w") as file:
                        file.write(f"USER LOGIN: {values['userlogin']}\nPASSWORD: {values['gen_pass']}")
                else:
                    actual_path = str(values['chosen_folder'])
                    mkd_path = os.path.join(actual_path, 'PWD GEN', values['categories'])
                    if not os.path.exists(mkd_path):
                        os.makedirs(f"{mkd_path}")
                    with open(f"{mkd_path}/{values['title']}.txt", mode = "w") as file:
                        file.write(f"USER LOGIN: {values['userlogin']}\nPASSWORD: {values['gen_pass']}")

        if event == 'OPEN DIR':
            if values['chosen_folder'] == '':
                if not os.path.exists(os.path.join(str(base_folder), 'PWD GEN')):
                    os.makedirs(os.path.join(str(base_folder), 'PWD GEN'))
                os.startfile(os.path.join(str(base_folder), 'PWD GEN'))
            else:
                if not os.path.exists(os.path.join(str(values['chosen_folder']), 'PWD GEN')):
                    os.makedirs(os.path.join(str(values['chosen_folder']), 'PWD GEN'))
                os.startfile(os.path.join(str(values['chosen_folder']), 'PWD GEN'))

        if event == 'CLEAR':
            cat_combo.update('PICK ONE')
            usertype_box.update('')
            title_input.update('')
            output.update('')
            cb_pass_txt.update(visible=False)


    window.close()

if __name__ == '__main__':
    main()