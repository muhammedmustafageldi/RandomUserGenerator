import requests
from tkinter import *
from PIL import Image, ImageTk
import pyperclip
from tkinter import filedialog
from datetime import datetime
from tkinter import messagebox
from io import BytesIO

root = Tk()

my_orange_color = '#e1830e'
my_white_color = '#dee1ec'
my_dark_color = '#5e6175'
my_light_color = '#bdc3d4'

full_name_variable = StringVar()
email_variable = StringVar()
birthday_variable = StringVar()
location_variable = StringVar()
phone_variable = StringVar()
password_variable = StringVar()


def window_settings():
    root.title(string='Random User Generator')
    root.iconbitmap('app_icon.ico')
    root.geometry('1200x720+300+200')
    root.config(background=my_dark_color)
    root.resizable(False, False)


def create_top_frame():
    top_frame = Frame(root, bg=my_light_color, height=65)
    top_frame.pack(fill='x')

    app_image = Image.open('app_icon.ico')
    resized_app_icon = app_image.resize((65, 65), Image.LANCZOS)
    app_icon = ImageTk.PhotoImage(resized_app_icon)

    label_app_icon = Label(top_frame, image=app_icon, bg=my_light_color)
    label_app_icon.image = app_icon
    label_app_icon.grid(row=0, column=0)

    label_app_name = Label(top_frame, text='Random User Generator', bg=my_light_color, fg='white',
                           font=('poppins', 25, 'bold'))
    label_app_name.grid(row=0, column=1, padx=10)

    top_frame.columnconfigure(2, weight=1)

    label_brand = Label(top_frame, text='Created by\nSwanky', bg=my_light_color, fg=my_orange_color,
                        font=('poppins', 10, 'bold'))
    label_brand.grid(row=0, column=2, padx=10, sticky="e")


def create_widgets():
    # User profile image
    test_img = create_image_with_path(path='app_icons/anonymous.png', x=128, y=128)

    label_user_img = Label(root, image=test_img)
    label_user_img.image = test_img
    label_user_img.pack(padx=10, pady=10)

    download_image = create_image_with_path('app_icons/download_button.png', 202, 40)
    download_button = Button(root, image=download_image, background=my_dark_color, borderwidth=0,
                             activebackground=my_dark_color, cursor='hand2')
    download_button.image = download_image

    # Name and surname
    name_img = create_image_with_path(path='app_icons/full_name_bg.png', x=300, y=50)
    label_name_bg = Label(root, image=name_img, background=my_dark_color)
    label_name_bg.image = name_img
    label_name_bg.pack()

    full_name_variable.set('...')
    label_name = Label(label_name_bg, width=20, justify='center', textvariable=full_name_variable,
                       font=('poppins', 15, 'bold'), background=my_light_color, foreground='white')
    label_name.pack(side='left')

    copy_name_image = create_image_with_path('app_icons/copy.png', x=26, y=26)
    copy_name_button = Button(label_name_bg, image=copy_name_image, borderwidth=0, background=my_light_color,
                              activebackground=my_light_color, cursor='hand2',
                              command=lambda: pyperclip.copy(full_name_variable.get()))
    copy_name_button.image = copy_name_image
    copy_name_button.pack(side='right')

    divider = Canvas(root, height=1, bg=my_light_color)
    divider.pack(fill="x", pady=10)

    # Other datas
    email_img = create_image_with_path('app_icons/email.png', x=32, y=32)
    create_frame_and_label(label_icon=email_img, label_variable=email_variable)

    birthday_img = create_image_with_path('app_icons/birthday.png', x=32, y=32)
    create_frame_and_label(label_icon=birthday_img, label_variable=birthday_variable)

    location_img = create_image_with_path('app_icons/location.png', x=32, y=32)
    create_frame_and_label(label_icon=location_img, label_variable=location_variable)

    call_img = create_image_with_path('app_icons/call.png', x=32, y=32)
    create_frame_and_label(label_icon=call_img, label_variable=phone_variable)

    password_img = create_image_with_path('app_icons/password.png', x=32, y=32)
    create_frame_and_label(label_icon=password_img, label_variable=password_variable)

    generate_bg = create_image_with_path(path='app_icons/create_button.png', x=344, y=57)
    generate_button = Button(root, image=generate_bg, background=my_dark_color, borderwidth=0, cursor='hand2',
                             activebackground=my_dark_color,
                             command=lambda: put_data_widgets(photo_label=label_user_img,
                                                              download_button=download_button))
    generate_button.image = generate_bg
    generate_button.pack(pady=20)


def create_frame_and_label(label_icon, label_variable):
    copy_image = Image.open('app_icons/copy.png')
    copy_icon = ImageTk.PhotoImage(copy_image.resize((32, 32), Image.LANCZOS))

    frame = Frame(root, bg=my_light_color, borderwidth=2, )
    frame.pack(pady=5)

    label_variable.set('...')

    label = Label(frame, justify='left', font=('poppins', 13, 'bold'), background=my_light_color, foreground='white',
                  bg=my_dark_color, textvariable=label_variable, padx=7,
                  image=label_icon, compound=LEFT, width=350, anchor='w')
    label.image = label_icon
    label.grid(row=0, column=0)

    copy_button = Button(frame, image=copy_icon, borderwidth=0, background=my_light_color,
                         activebackground=my_light_color,
                         cursor='hand2', command=lambda: pyperclip.copy(label_variable.get()))
    copy_button.image = copy_icon
    copy_button.grid(row=0, column=1, padx=10)


def create_image_with_path(path, x, y):
    opened_image = Image.open(path)
    return ImageTk.PhotoImage(opened_image.resize((x, y), Image.LANCZOS))


def get_user_data():
    url = 'https://randomuser.me/api/'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        result = data['results']
        user_details = result[0]

        name = user_details['name']
        first_name = name['first']
        surname = name['last']

        email = user_details['email']

        dob = user_details['dob']['date']
        birthday = format_date(dob)

        # Location
        street_number = user_details['location']['street']['number']
        street_name = user_details['location']['street']['name']
        city = user_details['location']['city']
        country = user_details['location']['country']

        full_street = f"{street_number} {street_name} {city}/{country}"

        phone = user_details['phone']
        password = user_details['login']['password']
        photo = user_details['picture']['large']

        user_desc = {
            'full_name': first_name + ' ' + surname,
            'email': email,
            'birthday': birthday,
            'full_street': full_street,
            'phone': phone,
            'password': password,
            'photo': photo
        }
        return user_desc
    else:
        messagebox.showerror(title='Error', message=f'Error. Request failed. HTTP code: {response.status_code}')


def put_data_widgets(photo_label, download_button):
    data_dict = get_user_data()
    if data_dict:
        fullname = data_dict.get('full_name')
        email = data_dict.get('email')
        birthday = data_dict.get('birthday')
        full_street = data_dict.get('full_street')
        phone = data_dict.get('phone')
        password = data_dict.get('password')
        photo = data_dict.get('photo')

        full_name_variable.set(fullname)
        email_variable.set(email)
        birthday_variable.set(birthday)
        location_variable.set(full_street)
        phone_variable.set(phone)
        password_variable.set(password)

        # Download user picture
        image_data = get_image_from_url(url=photo)
        if image_data:
            image_as_bytes = BytesIO(image_data)
            image = Image.open(image_as_bytes)
            photo_image = ImageTk.PhotoImage(image.resize((128, 128), Image.LANCZOS))
            photo_label.config(image=photo_image)
            photo_label.image = photo_image
            download_button.pack()
            download_button.config(command=lambda: save_image(image_data))
        else:
            messagebox.showwarning(title='Image error', message='There was an error uploading the photo')


def save_image(image_data):
    file_path = filedialog.asksaveasfilename(defaultextension='.jpg', filetypes=[("JPEG files", "*.jpg")],
                                             initialfile='profile.jpg')
    if file_path:
        try:
            with open(file_path, 'wb') as file:
                file.write(image_data)
                messagebox.showinfo('Save', message='Save is success.')
        except Exception as e:
            print(str(e))


def get_image_from_url(url):
    try:
        picture_response = requests.get(url)
        if picture_response.status_code == 200:
            image_data = picture_response.content
            return image_data
        else:
            return None
    except Exception as e:
        print('Exception of the picture.', str(e))
        return None


def format_date(api_date):
    date_object = datetime.strptime(api_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    just_date = date_object.strftime("%d-%m-%Y")
    return just_date


window_settings()
create_top_frame()
create_widgets()

root.mainloop()
