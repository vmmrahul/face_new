import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from pymysql import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage


def makeConnections():
    return connect(host='127.0.0.1', user='root', password='', database='library',
                   cursorclass=cursors.DictCursor)


def login(request):
    if 'admin' in request.session:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['Password']
        query = f"select `email`, `name`, `mobile`, `type` from admin where email='{email}' and password='{password}'"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        resut = cr.fetchall()
        print(resut)
        if len(resut) > 0:
            request.session['admin'] = resut[0]
            return redirect('dashboard')
        else:
            messages.warning(request, 'invalid Email or Password !!!')
            return redirect('loginPage')
    return render(request, 'adminWork/login.html')


def dashboard(request):
    return render(request, 'adminWork/dashboard.html')


def signout(request):
    try:
        del request.session['admin']
    except:
        pass
    return redirect('loginPage')


def changePassword(request):
    """
    in this function we are workin for change password
    :param request:
    :return :
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')

        query = f"select * from admin where email='{email}' and password='{oldPassword}'"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        resut = cr.fetchall()
        if len(resut) > 0:
            query = "UPDATE `admin` SET `password`='{}' WHERE `email`='{}'".format(newPassword, email)
            cr.execute(query)
            conn.commit()
            conn.close()
            messages.success(request, "Successfully Update password")

            return redirect('changePassword')
        else:
            messages.warning(request, 'Plz enter correct old Password!!!')
            return redirect('changePassword')
    return render(request, 'adminWork/changePassword.html')


def addLibrary(request):
    if request.method == 'POST':
        print(request.FILES)
        name = request.POST['name']
        location = request.POST['location']
        campusName = request.POST['campusName']
        departmentName = request.POST['departmentName']
        headLibrarian = request.POST['headLibrarian']
        mobile = request.POST['mobile']
        email = request.POST['email']
        password = request.POST['password']
        description = request.POST['description']
        photo = request.FILES['photo']
        query = "SELECT * FROM `library` where email='{}'".format(email)
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        result = cr.fetchall()
        if len(result) > 0:
            messages.warning(request, "Allready Email is taken.")
            return redirect('addLibrary')

        fs = FileSystemStorage()
        filename = fs.save('Library/' + photo.name, photo)
        query = f"INSERT INTO `library`(`name`, `location`, `campusName`, `departmentName`, `head_Librarian`, `mobile`, `email`, `password`, `photo`, `description`) VALUES('{name}','{location}','{campusName}','{departmentName}','{headLibrarian}','{mobile}','{email}','{password}','{filename}','{description}')"

        cr.execute(query)
        conn.commit()
        messages.success(request, "Success fully Added {}".format(name))
        return redirect('addLibrary')
    return render(request, 'adminWork/addLibrary.html')


def ViewLibrary(request):
    query = "SELECT * FROM `library`"
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    resut = cr.fetchall()
    return render(request, 'adminWork/viewLibrary.html', {'data': resut})


def deleteLibrary(request, id):
    query = "DELETE FROM `library` WHERE id ='{}'".format(id)
    print(query)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    messages.success(request, 'successFully delete !!')
    return redirect('ViewLibrary')


def editLibrary(request, id):
    query = "SELECT * FROM `library` where id='{}'".format(id)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    resut = cr.fetchall()
    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['name']
        location = request.POST['location']
        campusName = request.POST['campusName']
        departmentName = request.POST['departmentName']
        headLibrarian = request.POST['headLibrarian']
        mobile = request.POST['mobile']
        email = request.POST['email']
        password = request.POST['password']
        description = request.POST['description']
        filename = ""
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save('Library/' + photo.name, photo)
            filename = ",`photo`='{}'".format(filename)
        query = f"UPDATE `library` SET `name`='{name}',`location`='{location}',`campusName`='{campusName}',`departmentName`='{departmentName}',`head_Librarian`='{headLibrarian}',`mobile`='{mobile}',`email`='{email}',`password`='{password}'{filename},`description`='{description}' WHERE `id`='{id}'"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        conn.commit()
        messages.success(request, "Success fully Update {}".format(name))
        return redirect('ViewLibrary')
    return render(request, 'adminWork/editLibrary.html', {'data': resut[0]})


def addMeber(request):
    return render(request,'')





# Client Side Work

def userLogin(request):
    if 'userLogin' in request.session:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        query = "SELECT * FROM `library` where email='{}' and password ='{}'".format(email, password)
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        result = cr.fetchall()

        if len(result) > 0:
            request.session['userLogin'] = result[0]
            return redirect('home')
        else:
            messages.warning(request, 'Invalid Email or Password')
            return redirect('userLogin')

    return render(request, 'user/UserLogin.html')


def home(request):
    if not ('userLogin' in request.session):
        return redirect('userLogin')
    return render(request, 'user/index.html')


def Usersignout(request):
    try:
        del request.session['userLogin']
    except:
        pass
    return redirect('userLogin')


def addSection(request):
    if not ('userLogin' in request.session):
        return redirect('userLogin')
    if request.method == 'POST':
        library = request.session['userLogin']['id']
        name = request.POST.get('name')
        Descripiton = request.POST.get('Descripiton')
        Locations = request.POST.get('Locations')
        incharge = request.POST.get('incharge')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        query = f"INSERT INTO `section`(`library`, `name`, `description`, `location`, `sectionIncharge`, `email`, `mobile`) VALUES ('{library}','{name}','{Descripiton}','{Locations}','{incharge}','{email}','{mobile}')"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        conn.commit()
        messages.success(request, 'section Add Success Fully')
        return redirect('addSection')
    return render(request, 'user/addSections.html')


def viewSection(request):
    query = "SELECT * FROM `section` where `library` = '{}'".format(request.session['userLogin']['id'])
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    return render(request, 'user/viewSection.html', {'data': result})


def deleteSection(request):
    id = request.GET['id']
    query = "DELETE FROM `section` WHERE `id`='{}'".format(id)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    messages.success(request, 'Success Fully Deleted {}'.format(id))
    return redirect('viewSection')


def addbook(request):
    result = 'No'
    id = 'No'
    if 'id' not in request.GET:
        query = "SELECT id, name FROM `section`"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        result = cr.fetchall()
    else:
        id = request.GET['id']

    if request.method == "POST":
        section = request.POST['section']
        title = request.POST['title']
        ISBN = request.POST['ISBN']
        QTY = request.POST['QTY']
        Edition = request.POST['Edition']
        Descripiton = request.POST['Descripiton']
        Author = request.POST['Author']
        price = request.POST['price']
        query = f"INSERT INTO `books`(`ISBN`, `title`, `section`, `qty`, `edition`, `descripiton`, `author`, `price`) VALUES ('{ISBN}','{title}','{section}','{QTY}','{Edition}','{Descripiton}','{Author}','{price}')"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        conn.commit()
        messages.success(request, 'Successfully add book {}'.format(title))
        return redirect('addbook')
    return render(request, 'user/addBooks.html', {'result': result, 'id': id})


def viewBook(request):
    query = "SELECT books.id,books.ISBN, books.title,books.section,section.name as sectionName, books.qty,books.edition, books.descripiton,books.author,books.price FROM `books` INNER JOIN section on books.section = section.id"
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    return render(request, 'user/viewBooks.html', {'result': result})

def deleteBook(request):
    id =request.GET['id']
    query = "DELETE FROM `books` WHERE id='{}'".format(id)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    messages.warning(request, 'Successfully add book {}'.format(id))
    return redirect('viewBook')


def addEbook(request):
    result = 'No'
    id = 'No'
    if 'id' not in request.GET:
        query = "SELECT id, name FROM `section`"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        result = cr.fetchall()
    else:
        id = request.GET['id']

    if request.method == "POST":
        section = request.POST['section']
        title = request.POST['title']
        ISBN = request.POST['ISBN']
        Edition = request.POST['Edition']
        Descripiton = request.POST['Descripiton']
        Author = request.POST['Author']
        price = request.POST['price']
        photo = request.FILES['pdf']
        fs = FileSystemStorage()
        filename = fs.save('EBook/' + photo.name, photo)
        query = f"INSERT INTO `ebook`(`ISBN`, `title`, `section`,`edition`, `descripiton`, `author`, `price`,`file`) VALUES ('{ISBN}','{title}','{section}','{Edition}','{Descripiton}','{Author}','{price}','{filename}')"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        conn.commit()
        messages.success(request, 'Successfully add book {}'.format(title))
        return redirect('addEbook')
    return render(request, 'user/addEbooks.html', {'result': result, 'id': id})



def viewEBook(request):
    query ="SELECT ebook.id,ebook.ISBN, ebook.title,ebook.section,section.name as sectionName, ebook.edition, ebook.descripiton,ebook.author,ebook.price, ebook.file FROM `ebook` INNER JOIN section on ebook.section = section.id"
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    return render(request,'user/viewEbooks.html',{'result':result})


def deleteEbook(request):
    id =request.GET['id']
    query = "DELETE FROM `ebook` WHERE id='{}'".format(id)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    messages.warning(request, 'Successfully add book {}'.format(id))
    return redirect('viewEBook')