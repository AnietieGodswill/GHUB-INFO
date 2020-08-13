from tkinter import *
import requests
from bs4 import BeautifulSoup
import sys
import webbrowser
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox

        
def ghubinfo():
    global uname
    uname = ebox_email.get()
    url = "https://github.com/"+uname
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"html.parser")
    #for name
    find_name = soup.find("span",itemprop="name")
    find_name_text = find_name.text
    if len(find_name_text) > 1:
        listbox_1.delete(0,END)
        listbox_1.insert(1,f"Name: {find_name_text}")
    else:
        listbox_1.delete(0,END)
        listbox_1.insert(1,"Name: n/a")

    '''
    #for desc
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    find_desc = soup.find("div",class_="user-profile-bio")
    #print(find_desc.text.strip().translate(non_bmp_map))
    trans_desc = find_desc.text.strip().translate(non_bmp_map)
    if len(trans_desc) > 1:
        listbox_1.insert(1,f"Desc: {trans_desc}")
    else:
        listbox_1.insert(1,f"Desc: no description found")
    '''
    #follower,following,stars
    ffs = soup.findAll("span",class_="text-bold text-gray-dark")
    ffs_list =["Followers","Following","Stars"]
    for n,i in enumerate(ffs):
        store_i = i.text
        listbox_1.insert(2,f"{ffs_list[n]} : {store_i}")
        #listbox_1.insert(1,f"{ffs_list[n]} : n/a")
    '''
    #for organisation
    for_org = soup.find("span",class_="p-org")
    if len(for_org)>1:
        listbox_1.insert(2,f"Organization: {for_org.text}")
    else:
        listbox_1.insert(2,f"Organization: n/a")
    '''
    #for country
    find_cntry = soup.find("span",class_="p-label")
    find_cntry_text = find_cntry.text
    if len(find_cntry_text) > 1:
        listbox_1.insert(3,f"Country: {find_cntry_text}")
    else:
        listbox_1.insert(3,"Country: n/a")

    ghubrepo()

def ghubrepo():
    url1 = "https://github.com/"+uname+"?tab=repositories"
    r1 = requests.get(url1)
    soup1 = BeautifulSoup(r1.content,"html.parser")
    github_repo = soup1.findAll("a",itemprop="name codeRepository")
    listbox_2.delete(0,END)
    #repo_lang = soup1.findAll("span",itemprop="programmingLanguage")

    append_repo = []
    for i1 in github_repo:
        append_repo.append(i1.text.strip())

    append_k1 = []  
    for k1 in github_repo:
        href_k1 = k1.attrs["href"]
        add_k1 = "https://github.com"+href_k1
        append_k1.append(add_k1)

    n = 0
    for a in range(0,1000):
        try:
            n += 1
            listbox_2.insert(1,f"{append_repo[n]} : {append_k1[n]}")

        except IndexError:pass

def selection():
    try:
        value_get = listbox_2.get(listbox_2.curselection())
    except:
        messagebox.showerror("Error", "Select any repo to open")
    select_extract = value_get.split(":")[-1]
    final = "https:"+select_extract
    #print(final)
    webbrowser.open_new_tab(final) 
def repodown():
    try:
        value_get = listbox_2.get(listbox_2.curselection())
    except:
        messagebox.showerror("Error", "Select any repo to download")
    select_extract = value_get.split(":")[-1]
    final = "https:"+select_extract+"/archive/master.zip"
    #webbrowser.open_new_tab(final) 
    r = requests.get(final,stream=True)
    select_extract_1 = value_get.split(":")[:1]
    print(select_extract_1)
    with open(f"{select_extract_1}.zip",'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        

if __name__ == "__main__":
    root = Tk()
    root.title("GHUB-INFO - dx4iot")
    root.geometry("900x950")
    root.config(background="gray18")
    root.iconbitmap('icon.ico')
    root.resizable(0,0)

    h1 = Label(root,text="GHUB-INFO",font="Unispace 50 underline",bg="gray18",fg="white")
    h1.pack()
    frame_h1_n_ebox = Frame(root)
    frame_h1_n_ebox.config(background="gray18")
    frame_h1_n_ebox.pack()
    #for name
    ebox_email = Entry(frame_h1_n_ebox,font="Unispace 25",bg="gray18",fg="white",width=20)
    ebox_email.insert(0,"ENTER USERNAME")
    ebox_email.pack(pady=10,padx=10,side=LEFT)
    #for button
    ebox_send = Button(frame_h1_n_ebox,text='SEARCH', command=ghubinfo,font='Unispace 18',width=15)
    ebox_send.pack(pady=10,side=LEFT)
    #for heading 2
    h2 = Label(root,text="General Information",font="Unispace 30",bg="gray18",fg="white")
    h2.pack(pady=10)
    #for frame 1
    frame_1 = Frame(root)
    frame_1.config(background='gray18')
    frame_1.pack()
    #for listbox_1
    listbox_1 = Listbox(frame_1,font="Unispace 20",width=50,height=6,bg="gray18",fg="white")
    listbox_1.pack(pady=10)
    #for heading 3
    h3 = Label(root,text="Repositories",font="Unispace 30",bg="gray18",fg="white")
    h3.pack(pady=10)
    #for frame 2
    frame = Frame(root)
    frame.config(background='gray')
    frame.pack()
    #for listbox_2
    listbox_2 = Listbox(frame,font="Unispace 20",width=50,height=6,bg="gray18",fg="white")
    listbox_2.pack(pady=10,side="left", fill="y")
    scrollbar = Scrollbar(frame, orient="vertical")
    scrollbar.config(command=listbox_2.yview)
    scrollbar.pack(side="right",fill="y")
    listbox_2.config(yscrollcommand=scrollbar.set)


    #frame 3
    frame_3 = Frame(root)
    frame_3.config(background="gray18")
    frame_3.pack(padx=5, pady=20)

    b2 = Button(frame_3, text='OPEN REPO',command=selection,font='Unispace 20',width=15)
    b2.pack(padx=5, pady=5,side=LEFT)
    b3 = Button(frame_3, text='DOWNLOAD REPO',font='Unispace 20',width=15,command=repodown)
    b3.pack( padx=5, pady=5,side=LEFT)

    footer = Label(root,text="Developed By: dx4iot",font="Unispace 20 ",bg="gray18",fg="white")
    footer.pack(pady=10)
    root.mainloop()

