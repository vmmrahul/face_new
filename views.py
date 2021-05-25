import datetime

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
    if request.method == 'POST':
        print(request.POST)
        dateofJoin = request.POST['dateofJoin']
        campus = request.POST['campus']
        department = request.POST['department']
        typeofmember = request.POST['typeofmember']
        nocDate = request.POST['nocDate']
        membershipStatus = request.POST['membershipStatus']
        remarks = request.POST['remarks']
        query = f"INSERT INTO `membership`(`dateofjoining`, `campus`, `department`, `typeOfMember`, `membershipStatus`, `nocDate`, `remarks`) VALUES ('{dateofJoin}','{campus}','{department}','{typeofmember}','{membershipStatus}','{nocDate}','{remarks}')"
        print(query)
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        conn.commit()
        messages.success(request, 'Success Fully member added.')
    return render(request, 'adminWork/addMember.html')


def viewMembers(request):
    status = request.GET['status']
    query = "SELECT * FROM `membership` WHERE `membershipStatus`='{}'".format(status)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    columnName = [name[0] for name in cr.description]
    print(columnName)
    return render(request, 'adminWork/viewMember.html', {'status': status, 'result': result, 'columnName': columnName})


def changeMemberStatus(request):
    id = request.GET['id']
    status = request.GET['status']

    query = "UPDATE `membership` SET `membershipStatus`='{}' WHERE `id` ='{}'".format(status, id)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    messages.success(request, 'Success Fully Updated Member Status')
    return HttpResponseRedirect('viewMembers?status={}'.format(status))


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

    return render(request, 'library/UserLogin.html')


def home(request):
    if not ('userLogin' in request.session):
        return redirect('userLogin')
    return render(request, 'library/index.html')


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
    return render(request, 'library/addSections.html')


def viewSection(request):
    query = "SELECT * FROM `section` where `library` = '{}'".format(request.session['userLogin']['id'])
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    return render(request, 'library/viewSection.html', {'data': result})


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
    return render(request, 'library/addBooks.html', {'result': result, 'id': id})


def viewBook(request):
    if 'memberid' in request.GET:
        memberid = request.GET['memberid']
    else:
        memberid = 'No'
    query = "SELECT books.id,books.ISBN, books.title,books.section,section.name as sectionName, books.qty,books.edition, books.descripiton,books.author,books.price FROM `books` INNER JOIN section on books.section = section.id"
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    return render(request, 'library/viewBooks.html', {'result': result, 'memberid': memberid})


def deleteBook(request):
    id = request.GET['id']
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
    return render(request, 'library/addEbooks.html', {'result': result, 'id': id})


def viewEBook(request):
    query = "SELECT ebook.id,ebook.ISBN, ebook.title,ebook.section,section.name as sectionName, ebook.edition, ebook.descripiton,ebook.author,ebook.price, ebook.file FROM `ebook` INNER JOIN section on ebook.section = section.id"
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    return render(request, 'library/viewEbooks.html', {'result': result})


def deleteEbook(request):
    id = request.GET['id']
    query = "DELETE FROM `ebook` WHERE id='{}'".format(id)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    messages.warning(request, 'Successfully add book {}'.format(id))
    return redirect('viewEBook')


def viewActiveMember(request):
    query = "SELECT `id`, `dateofjoining`, `campus`, `department`, `typeOfMember` FROM `membership` WHERE `membershipStatus`='Active'"
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    columnName = [name[0] for name in cr.description]
    print(columnName)
    return render(request, 'library/activeMembers.html', {'result': result, 'columnName': columnName})


def ishuBook(request):
    bookid = request.GET['bookid']
    memberid = request.GET['memberid']
    todaydate = datetime.date.today()
    expDire = todaydate + datetime.timedelta(14)

    query = "select * from `transaction` where `membershipId`='{}' and bookid='{}' and Fine is null".format(memberid,bookid)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    if len(result)>0:
        messages.warning(request,'Book already issud to member id: {}'.format(memberid))
    else:
        query = f"INSERT INTO `transaction`(`bookid`, `membershipId`, `dateofissue`, `dateofReturn`) VALUES ('{bookid}','{memberid}','{todaydate}','{expDire}')"
        cr.execute(query)
        conn.commit()
        messages.success(request,'Book ishu to member id: {}'.format(memberid))
    return redirect('viewActiveMember')

def viewIshuBooks(request):
    id = request.GET['memberid']
    status = request.GET['status']
    todaydate = datetime.date.today()
    if status == 'current':
        query ="SELECT * FROM `transaction` where membershipId = '{}' and fine is null and `dateofReturn` > '{}'".format(id, todaydate)
    elif status == 'return':
        query = "SELECT * FROM `transaction` where membershipId = '{}' and fine is not null".format(id)
    else:
        query = "SELECT * FROM `transaction` where membershipId = '{}' and fine is null and `dateofReturn` < '{}'".format(id,todaydate)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    print(result)
    return render(request, 'library/viewIsshuBooks.html',{'memberid':id,'results':result,'status':status})

def collectFine(request):
    id = request.GET['memberid']
    status = request.GET['status']

    todaydate = datetime.date.today()
    issuID = request.POST['issuID']
    fine = request.POST['fine']
    payment = request.POST['payment']


    query =f"UPDATE `transaction` SET `Fine`='{fine}',`fine_collect_date`='{todaydate}',`mode_of_payment`='{payment}' WHERE  `tid`='{issuID}'"

    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    messages.success(request, 'Success Fully Collected fine')
    return HttpResponseRedirect(f'viewIshuBooks?memberid={id}&status={status}')


def index(request):
    return render(request, 'user/index.html')

def searchebooks(request):
    return render(request,'user/viewE-books.html')

def searchebooksAction(request):
    search_query = request.GET['searchquery']
    if search_query == 'all':
        query ="SELECT * FROM `ebook`"
    else:
        query = "SELECT * FROM `ebook` where title like '%{0}%' or author like '%{0}%'".format(search_query)
    print(query)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    return JsonResponse({'content':result})

def searchBooks(request):
    return render(request, 'user/viewBooks.html')


def searchbooksAction(request):
    search_query = request.GET['searchquery']
    if search_query == 'all':
        query ="SELECT books.title, books.edition, books.author, books.qty, library.name, section.name as section FROM `books` INNER JOIN section on section.id = books.section INNER JOIN library on section.library = library.id"
    else:
        query = "SELECT books.title, books.edition, books.author, books.qty, library.name, section.name as section  FROM `books` INNER JOIN section on section.id = books.section INNER JOIN library on section.library = library.id WHERE books.title like '%{0}%' or books.author like '%{0}%'".format(search_query)
    print(query)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    return JsonResponse({'content':result})


import smtplib
import email.message

def checkthis(name, emails, subject, msgs):
    receiver = 'neek3190@gmail.com '
    username = 'Admin'
    mobile = '6280995201'

    sender = 'python.vmm.2020@gmail.com'
    password = 'PythonVmm2021'

    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(sender, password)
    print("-----> Hello")
    body = f"""
                <html>
                <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                </head>
                <body>
                    <table  width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4"">
                    <tr>
                        <td>Name: </td>
                        <td> {name}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td></td>
                        <td>Email: </td>
                        <td>{emails}</td>
                    </tr>
                    <tr>
                        <td></td>
                        <td>Subject: </td>
                        <td>{subject}</td>
                    </tr>
                    <tr>
                        <td></td>
                        <td>Message: </td>
                        <td>{msgs}</td>
                    </tr>
                </table>
            </body>
                """

    print(email.message.Message())
    msg = email.message.Message()
    msg['Subject'] = 'Rss News Feed'

    msg['From'] = sender
    msg['To'] = receiver
    password = password
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(body)

    smtpserver.sendmail(sender, receiver, msg.as_string())
    print('Sent')
    smtpserver.close()
    return True



def contactUs(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        msg = request.POST['message']
        result = checkthis(name=name, emails=email, subject=subject, msgs=msg)
        if result:
            messages.success(request, 'Thank you we will reach you soon')
        else:
            messages.success(request, 'Fail due to some Tech ishu!!!!')
        return redirect('contactUs')
    return render(request, 'user/contactus.html')
