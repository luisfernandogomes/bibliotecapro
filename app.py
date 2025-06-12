import flet as ft
from flet import AppBar, Text, View
from flet.core.colors import Colors

from flet.core.textfield import TextField

from funcoes_api import *


def main(page: ft.Page):
    # Configurações
    page.title = "Biblioteca Gomes"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    # def lista_em_detalhes(e):
    #     lv_Descricao.controls.clear()
    #     for livro in lista:
    #         lv_Descricao.controls.append(
    #             ft.ListTile(
    #                 leading=ft.Icon(ft.Icons.PERSON),
    #                 title=ft.Text(livro.nome),
    #                 subtitle=ft.Text(livro.autor),
    #                 trailing=ft.PopupMenuButton(
    #                     icon=ft.Icons.MORE_VERT,
    #                     items=[
    #                         ft.PopupMenuItem(text='detalhes',on_click=lambda _: page.go('/terceira')),
    #                     ]
    #                 )
    #             )
    #         )
    #     page.update()
    # def exibir_banco_em_detalhes(e):
    #     lv_Descricao.controls.clear()
    #     user = get_usuarios()
    #     livros = db_session.execute(select(Livro)).scalars()
    #     for livro in livros:
    #         lv_Descricao.controls.append(
    #             ft.ListTile(
    #                 leading=ft.Icon(ft.Icons.BOOK),
    #                 title=ft.Text(user['nome']),
    #                 subtitle=ft.Text(livro.autor),
    #                 trailing=ft.PopupMenuButton(
    #                                         icon=ft.Icons.MORE_VERT,
    #                                         items=[
    #                                             ft.PopupMenuItem(text='detalhes',on_click=lambda _, l=livro: exibir_detalhesuu(l)),
    #
    #                                         ]
    #                                     )
    #                                 )
    #                             )
    #     page.update()


    lista = []
    # Funções
    # def exibir_banco(e):
    #     livros = db_session.execute(select(Livro)).scalars()
    #     lv_Descricao.controls.clear()
    #     for livro in livros:
    #         lv_Descricao.controls.append(
    #             ft.Text(value=f'Nome do livro: {livro.nome}\nDescricao do livro: {livro.descricao}\nAutor do livro: {livro.autor}\n categoria: {livro.categoria}\n INSBN: {livro.ISBN}')
    #         )




    # def exibir_lista(e):
    #     print('teste')
    #     lv_Descricao.controls.clear()
    #     for livro in lista:
    #         lv_Descricao.controls.append(
    #             ft.Text(value=f'nome do livro {livro.nome} \ndescrição: {livro.descricao}\nautor: {livro.autor}')
    #         )
    # def detalhes(e,id_do_livro):


    # def salvar_livro(e):
    #     if input_nome.value == '' or input_descricao.value == '' or input_autor.value == '':
    #         page.overlay.append(msg_error)
    #         msg_error.open = True
    #         page.update()
    #     elif input_isbn.value in lista:
    #         page.overlay.append(msg_error)
    #         msg_error.open = True
    #         page.update()
    #     else:
    #         livro = Livro(nome=input_nome.value, descricao=input_descricao.value, autor=input_autor.value, categoria=input_categoria.value, ISBN=input_isbn.value)
    #         livro.save()
    #         input_nome.value = ''
    #         input_descricao.value = ''
    #         input_autor.value = ''
    #         input_categoria.value = ''
    #         input_isbn.value = ''
    #         page.overlay.append(msg_sucesso)
    #         msg_sucesso.open = True
    #         page.update()

    icone = ft.Icon(ft.Icons.PERSON,size=100)


    def mostrar_livros(e):
        lv_Descricao.controls.clear()
        dados = get_livros()

        for book in dados:
            def teste(book):
                if book['status']:
                    return ft.Icon(ft.Icons.BOOK,color=Colors.GREEN)
                else:
                    return ft.Icon(ft.Icons.BOOK,color=Colors.RED)
            iconbook = teste(book)
            lv_Descricao.controls.append(


                ft.ListTile(
                    leading=iconbook,
                    title=ft.Text(book['titulo'], color='#153147'),
                    subtitle=ft.Text(book['autor'], color='#153147'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_HORIZ_OUTLINED, icon_color=Colors.BLACK,
                        items=[
                            ft.PopupMenuItem(text='detalhes do livro', on_click=lambda _, u=book: detalhes_do_livro(u)),
                            ft.PopupMenuItem(text='Editar livro', on_click=lambda _, u=book: editar_livro(u)),
                            ft.PopupMenuItem(text='realizar emprestimo', on_click=lambda _, u=book: realizar_emprestimo(u)),
                            # ft.PopupMenuItem(text='realizar emprestimo', on_click=lambda _: page.go('realizar_emprestimo'))

                        ], bgcolor='#153147'
                    )
                ))
            page.update()

    msg_error_emprestimo = ft.SnackBar(
        content=ft.Text(value='O livro não está disponivel para emprestimos temporariamente'),
        bgcolor=Colors.RED,
        duration=2000,
    )


    def editar_livro(book):
        campo_id_livro.value = book['id do livro']
        campo_titulo.value = book['titulo']
        campo_autor.value = book['autor']
        campo_resumo.value = book['resumo']
        campo_ISBN.value = book['ISBN']
        page.go('/editar_livro')



    ISBN = ft.Text('',color='#153147')
    titulo = ft.Text('',color='#153147')
    autor = ft.Text('',color='#153147')
    resumo = ft.Text('',color='#153147')
    status = ft.Text('',color='#153147')
    id_do_livro = ft.Text('',color='#153147')
    def detalhes_do_livro(book):
        if not book['status']:
            n.color = Colors.RED
        else:
            n.color = Colors.GREEN
        id_do_livro.value = book['id do livro']
        ISBN.value = book['ISBN']
        titulo.value = book['titulo']
        autor.value = book['autor']
        resumo.value = book['resumo']
        if book['status']:
            status.value = 'Livro está disponivel para emprestimo'
        else:
            status.value = 'Livro não está disponivel para emprestimo'
        page.go('/detalhes')

    def mostrar_emprestimos(e):
        lv_Descricao.controls.clear()
        dados = get_emprestimos()

        for emprestimo in dados:
            if emprestimo['status'] == 'pendente':
                icone_pendente = ft.Icon(ft.Icons.BOOK, color=Colors.RED)
            else:
                icone_pendente = ft.Icon(ft.Icons.BOOK, color=Colors.GREEN)
            lv_Descricao.controls.append(
                ft.ListTile(
                    leading=icone_pendente,
                    title=ft.Text(emprestimo['livro']['titulo'], color='#153147'),
                    subtitle=ft.Text(emprestimo['usuario']['nome'], color='#153147'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_HORIZ_OUTLINED, icon_color=Colors.BLACK,
                        items=[
                            ft.PopupMenuItem(text='detalhes', on_click=lambda _, u=emprestimo: detalhes_do_emprestimo(u)),
                            ft.PopupMenuItem(text='Finalizar emprestimo', on_click=lambda _, u=emprestimo: post_devolver_livro(u)),

                        ], bgcolor='#153147'
                    )
                ))
    def post_devolver_livro(emprestimo):
        if emprestimo['status'] == 'finalizado':
            abu = ft.Text('Este emprestimo já foi finalizado')
            snack_personalizado = ft.SnackBar(content=abu, bgcolor=Colors.RED, duration=2000)
            page.overlay.append(snack_personalizado)
            snack_personalizado.open = True
            page.update()
            return page.go('/biblioteca')
        dados = devolver_livro(emprestimo['livro']['ISBN'], emprestimo['usuario']['id'])
        if 'error' in dados:
            print('entrou no error')

        page.overlay.append(msg_sucesso)
        msg_sucesso.open = True
        page.go('/biblioteca')
        page.update()

    n = ft.Icon(ft.Icons.BOOK)
    def detalhes_do_emprestimo(emprestimo):
        id_emprestimo.value = emprestimo['id_emprestimo']
        data_emprestimo.value = emprestimo['data_emprestimo']
        data_de_devolucao.value = emprestimo['data_de_devolucao']
        emprestimo_usuario_id.value = emprestimo['usuario']['id']
        emprestimo_usuario_nome.value = emprestimo['usuario']['nome']
        emprestimo_usuario_CPF.value = emprestimo['usuario']['CPF']
        emprestimo_usuario_endereco.value = emprestimo['usuario']['endereco']
        emprestimo_livro_isbn.value = emprestimo['livro']['ISBN']
        emprestimo_livro_titulo.value = emprestimo['livro']['titulo']
        if emprestimo['livro']['status']:
            emprestimo_livro_status.value = 'livro já foi devolvido'
            n.color = Colors.GREEN
        else:
            emprestimo_livro_status.value = 'Livro ainda não foi devolvido'
            n.color = Colors.RED
        page.go('/detalhe_emprestimo')
    def mostrar_usuario(e):
        lv_Descricao.controls.clear()
        dados = get_usuarios()
        for user in dados:
            # lv_Descricao.controls.append(ft.Text(value=f'{user['nome']}\n{user['CPF']}\n{user['endereco']}',
            #                                      color=Colors.BLACK))

            lv_Descricao.controls.append(

                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),icon_color='#153147',
                    title=ft.Text(user['nome'],color='#153147'),
                    subtitle=ft.Text(user['CPF'],color='#153147'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_HORIZ_OUTLINED,icon_color=Colors.BLACK,
                        items=[
                            ft.PopupMenuItem(text='detalhes',on_click=lambda _, u=user: exibir_detalhesuu(u)),
                            ft.PopupMenuItem(text='Editar usuario',on_click=lambda _, u=user: editar_usuario(u)),
                            ft.PopupMenuItem(text='Emprestimos do usuario',on_click=lambda _, u=user: emprestimos_que_usuario_tem(u)),
                        ],bgcolor='#153147'
                    )
                ))
            page.update()
    def emprestimos_que_usuario_tem(user):
        lv_Descricao.controls.clear()
        dados = get_emprestimos_por_usuario(user['id'])
        print(dados)
        for abu in dados:
            lv_Descricao.controls.append(ft.Text(value='data de devolução ' + abu['data_de_devolucao'],color=Colors.BLACK))
            lv_Descricao.controls.append(ft.Text(value='data do emprestimo ' + abu['data_emprestimo'],color=Colors.BLACK))
            lv_Descricao.controls.append(ft.Text(value=abu['id_emprestimo'],color=Colors.BLACK))
            lv_Descricao.controls.append(ft.Text(value=abu['livro']['ISBN'],color=Colors.BLACK))
            if abu['livro']['status']:
                lv_Descricao.controls.append(ft.Text(value='Livro já foi devolvido',color=Colors.BLACK))
            else:
                lv_Descricao.controls.append(ft.Text(value='Livro ainda não foi devolvido',color=Colors.BLACK))
            lv_Descricao.controls.append(ft.Text(value='Titulo ' + abu['livro']['titulo'],color=Colors.BLACK))
            lv_Descricao.controls.append(ft.Text(value='CPF do usurio ' + abu['usuario']['CPF'],color=Colors.BLACK))
            lv_Descricao.controls.append(ft.Text(value='Endereço do usuario ' + abu['usuario']['endereco'],color=Colors.BLACK))
            lv_Descricao.controls.append(ft.Text(value='Nome do usuario ' + abu['usuario']['nome'],color=Colors.BLACK))
        page.go('/emprestimo_usuario')



    def exibir_detalhesuu(user):
        nome_usuario.value = 'Nome: ' + user['nome']
        cpf_usuario.value = 'CPF: ' + user['CPF']
        endereco_usuario.value = 'descricao: ' + user['endereco']
        page.go('/detalhes_usuario')
    campo_id = ft.Text('',color='#153147',size=25)
    campo_nome = ft.TextField('',color='#153147')
    campo_cpf = ft.TextField('',color='#153147')
    campo_endereco = ft.TextField('',color='#153147')
    msg_errror_vazios = ft.SnackBar(
        content=ft.Text(value='Os campos estão vazios'),
        bgcolor=Colors.RED,
        duration=2000,
    )
    def salvar_usuario(e):
        if campo_user_nome.value == '' or campo_user_CPF.value == '' or campo_user_endereco.value == '':
            page.overlay.append(msg_errror_vazios)
            msg_errror_vazios.open = True
            return page.update()
        dados = post_usuario(campo_user_nome.value,campo_user_CPF.value,campo_user_endereco.value)
        if 'error' in dados:
            campo_user_nome.value = ""
            campo_user_CPF.value = ""
            campo_user_endereco.value = ""
            abu = ft.Text(value=dados['error'])
            snack_personalizado = ft.SnackBar(content=abu, bgcolor=Colors.RED, duration=2000)
            page.overlay.append(snack_personalizado)
            snack_personalizado.open = True
            return page.update()
        else:
            campo_user_nome.value = ""
            campo_user_CPF.value = ""
            campo_user_endereco.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()
            page.go('/usuarios')
            page.update()


    def editar_usuario(user):
        campo_id.value = user['id']
        campo_nome.value = user['nome']
        campo_cpf.value = user['CPF']
        campo_endereco.value = user['endereco']
        page.go('/editar_usuario')

    def salvar_livro(e):
        if (campo_book_titulo.value == '' or campo_book_autor.value == '' or campo_book_resumo.value == ''
                or campo_book_ISBN.value == ''):
            page.overlay.append(msg_errror_vazios)
            msg_errror_vazios.open = True
            return page.update()
        dados = post_livro(campo_book_titulo.value,campo_book_autor.value,campo_book_resumo.value,campo_book_ISBN.value)
        if 'error' in dados:
            abu = ft.Text(value=dados['error'])
            snack_personalizado = ft.SnackBar(content=abu, bgcolor=Colors.RED, duration=2000)
            page.overlay.append(snack_personalizado)
            snack_personalizado.open = True
            return page.update()
        else:
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()
            page.go('/biblioteca')

    def gerencia_rotas(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Home"), bgcolor='#153147',actions=[livro,perfil,opcoes],
                           leading=logo,center_title=True,color='#ffe6d9'),

                    logo2,
                    ft.Text(value="Bem-vindo à Biblioteca Gomes! ",
                            style=ft.TextStyle(size=15,color='#272123',font_family='Bahnschrift SemiLight Condensed',weight=ft.FontWeight.BOLD)),
                    ft.Text(value="   Na Biblioteca Gomes, você pode realizar empréstimos com diversas"
                                  " funcionalidades que facilitam sua experiência.",size=15,
                           style=ft.TextStyle(size=15,color='#272123',font_family='Bahnschrift SemiLight Condensed')),
                    ft.Text(value="   Aqui, é possível encontrar uma ampla variedade de livros, além de filtrar"
                                  " suas buscas por categorias ou autores, tornando a sua pesquisa muito mais prática"
                                  " e eficiente.",style=ft.TextStyle(size=15,color='#272123',font_family='Bahnschrift SemiLight Condensed')),


                    # ft.Button(
                    #     text="Salvar",
                    #     on_click=lambda _: salvar_livro(e),
                    # ),
                    # ft.Button(
                    #     text="Exibir",
                    #     on_click=lambda _: page.go('/livros'),
                    # )
                ],bgcolor='#E0DFDB',horizontal_alignment=ft.CrossAxisAlignment.CENTER,padding=50,vertical_alignment=ft.MainAxisAlignment.CENTER
            )
        )


        if page.route == "/biblioteca" or page.route == "/detalhes":
            mostrar_livros(e)

            page.views.append(
                View(
                    "/biblioteca",
                    [
                        AppBar(title=Text("Catalogo de livros"), bgcolor='#153147',actions=[perfil],leading=logo,center_title=True,color='#ffe6d9'),
                        lv_Descricao,


                        # ft.FloatingActionButton('+', on_click=detalhes(e))
                    ],bgcolor='#E0DFDB'
                )
            )



        if page.route == "/detalhes" or page.route == "/editar_livro":
            page.views.append(
                View(
                    "/detalhes",
                    [
                        AppBar(title=Text("Detalhes"), bgcolor='#153147',actions=[perfil],leading=logo,center_title=True,color='#ffe6d9'),
                        n,
                        id_do_livro,
                        ISBN,
                        titulo,
                        autor,
                        resumo,
                        status

                    ],bgcolor='#E0DFDB',horizontal_alignment=ft.CrossAxisAlignment.CENTER,padding=10,vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )



        if page.route == "/editar_livro" or page.route == "/cadastrar_usuario":
            page.views.append(
                View(
                    "/editar_livro",
                    [
                        AppBar(title=Text("Editar Usuario"), bgcolor='#153147',actions=[perfil],leading=logo,center_title=True,color='#ffe6d9'),
                        ft.Icon(ft.Icons.BOOK,size=100,color=Colors.BLACK),
                        campo_id_livro,
                        campo_titulo,
                        campo_autor,
                        campo_resumo,
                        campo_ISBN,
                        ft.Button(text='Salvar',on_click=salvar_editar_livro),
                        ft.Button(text='Voltar',on_click=lambda _: page.go('/biblioteca')),
                    ],bgcolor='#E0DFDB',horizontal_alignment=ft.CrossAxisAlignment.CENTER,padding=10,vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )




        if page.route == "/cadastrar_usuario" or page.route == "/cadastrar_emprestimo":
            page.views.append(
                View(
                    "/cadastrar_usuario",
                    [
                        AppBar(title=Text("Cadastrar usuario"), bgcolor='#153147',actions=[perfil],leading=logo,center_title=True,color='#ffe6d9'),
                        ft.Icon(ft.Icons.BOOK, size=200, color=Colors.BLACK),
                        campo_user_id,
                        campo_user_nome,
                        campo_user_CPF,
                        campo_user_endereco,
                        ft.Button(text='Salvar novo usuario', on_click=salvar_usuario),

                    ],bgcolor='#E0DFDB',horizontal_alignment=ft.CrossAxisAlignment.CENTER,padding=10,vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )



        if page.route == "/cadastrar_emprestimo" or page.route == "/cadastrar_livro":
            page.views.append(
                View(
                    "/cadastrar_emprestimo",
                    [
                        AppBar(title=Text("Cadastrar Emprestimo"), bgcolor='#153147', actions=[perfil], leading=logo, center_title=True,
                               color='#ffe6d9'),
                        ft.Icon(ft.Icons.BOOK, size=200, color=Colors.BLACK),

                    ],bgcolor='#E0DFDB',horizontal_alignment=ft.CrossAxisAlignment.CENTER,padding=10,vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )



        if page.route == "/cadastrar_livro" or page.route == "/usuarios":
            page.views.append(
                View(
                    "/cadastrar_livro",
                    [
                        AppBar(title=Text("Cadastrar Livro"), bgcolor='#153147',actions=[perfil],leading=logo,center_title=True,color='#ffe6d9'),
                        ft.Icon(ft.Icons.BOOK,size=200,color=Colors.BLACK),
                        campo_book_titulo,
                        campo_book_autor,
                        campo_book_resumo,
                        campo_book_ISBN,

                        ft.Button(text='Salvar',on_click=salvar_livro),
                    ],bgcolor='#E0DFDB',horizontal_alignment=ft.CrossAxisAlignment.CENTER,padding=10,vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )



        if page.route == "/usuarios" or page.route == "/detalhes_usuario":
            mostrar_usuario(e)
            page.views.append(
                View(
                    "/usuarios",
                    [
                        AppBar(title=Text("Usuarios"), bgcolor='#153147', actions=[perfil], leading=logo,
                               center_title=True, color='#ffe6d9'),
                        # ft.Button(
                        #     text='dada',
                        #     on_click=lambda _: mostrar_usuario(e),
                        # ),
                        lv_Descricao,


                    ],bgcolor='#E0DFDB'
                )
            )

        if page.route == "/detalhes_usuario" or page.route == "/editar_usuario":

            page.views.append(
                View(
                    "/detalhes_usuario",
                    [
                        AppBar(title=Text("usuario detalhado"), bgcolor='#153147',actions=[perfil],leading=logo,center_title=True,color='#ffe6d9'),
                        icone,
                        nome_usuario,
                        cpf_usuario,
                        endereco_usuario,
                        ft.Button(text='Voltar',on_click=lambda _: page.go('/usuarios')),


                    ],bgcolor='#E0DFDB',horizontal_alignment=ft.CrossAxisAlignment.CENTER,padding=10,vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )

        if page.route == "/editar_usuario" or app.route == "emprestimos":

            page.views.append(
                View(
                    "/editar_usuario",
                    [
                        AppBar(title=Text("Editar usuario"), bgcolor='#153147', actions=[perfil], leading=logo,
                               center_title=True, color='#ffe6d9'),
                        icone,
                        campo_id,
                        campo_nome,
                        campo_cpf,
                        campo_endereco,
                        ft.Button(text='Salvar',on_click=salvar_atualizacao),


                    ],bgcolor='#E0DFDB',horizontal_alignment=ft.CrossAxisAlignment.CENTER,padding=10,vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )
        if page.route == "/emprestimos" or page.route == "/detalhe_emprestimo":
            mostrar_emprestimos(e)
            page.views.append(
                View(
                    "/emprestimos",
                    [
                        AppBar(title=Text("Emprestimos"), bgcolor='#153147',actions=[perfil],leading=logo,center_title=True,color='#ffe6d9'),
                        lv_Descricao,
                    ],bgcolor='#E0DFDB',horizontal_alignment=ft.CrossAxisAlignment.CENTER,padding=10,vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )
        if page.route == "/detalhe_emprestimo" or page.route == "/realizar_emprestimo":
            page.views.append(
                View(
                    "/detalhe_emprestimo",
                    [
                        AppBar(title=Text("Emprestimo detalhado"), bgcolor='#153147',actions=[perfil],leading=logo,center_title=True,color='#ffe6d9'),
                        # 'id_emprestimo': emp.id_emprestimo,
                        # 'data_emprestimo': emp.data_emprestimo,
                        # 'data_de_devolucao': emp.data_de_devolucao,
                        # 'usuario': {
                        #     'id': emp.usuario.id,
                        #     'nome': emp.usuario.nome,
                        #     'CPF': emp.usuario.CPF,
                        #     'endereco': emp.usuario.endereco
                        # },
                        # 'livro': {
                        #     'ISBN': emp.livro.ISBN,
                        #     'titulo': emp.livro.titulo,
                        #     'status': emp.livro.status
                        n,
                        ft.Text(value='Dados do emprestimo',color=Colors.BLACK),
                        id_emprestimo,
                        data_emprestimo,
                        data_de_devolucao,
                        ft.Text(value='Dados do usuario que realizou emprestimo',color=Colors.BLACK),
                        emprestimo_usuario_id,
                        emprestimo_usuario_nome,
                        emprestimo_usuario_CPF,
                        emprestimo_usuario_endereco,
                        ft.Text(value='Dados do Livro', color=Colors.BLACK),
                        emprestimo_livro_isbn,
                        emprestimo_livro_titulo,
                        emprestimo_livro_status


                    ],bgcolor='#E0DFDB',horizontal_alignment=ft.CrossAxisAlignment.CENTER,padding=10,vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )
        if page.route == "/realizar_emprestimo" or page.route == "/emprestimo_usuario":
            page.views.append(
                View(
                    "/realizar_emprestimo",
                    [
                        AppBar(title=Text("Realizar emprestimo"), bgcolor='#153147',actions=[perfil],leading=logo,center_title=True,color='#ffe6d9'),

                        campo_user_post_emprestimo,
                        id_book_para_emprestimo,
                        titulo_book_para_emprestimo,

                        ft.Button(text='Realizar Emprstimo',on_click=lambda _: executar_emprestimo(e)),
                    ],bgcolor='#E0DFDB',horizontal_alignment=ft.CrossAxisAlignment.CENTER,padding=10,vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )
        if page.route == '/emprestimo_usuario':
            page.views.append(
                View(
                    '/emprestimo_usuario',
                    [
                        AppBar(title=Text("emprestimo usuario"), bgcolor='#153147', actions=[perfil], leading=logo,
                               center_title=True, color='#ffe6d9'),
                        lv_Descricao


                    ],bgcolor='#E0DFDB',horizontal_alignment=ft.CrossAxisAlignment.CENTER,padding=10,vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )
        page.update()
    # c = ft.Dropdown.Option(text=)
    id_book_para_emprestimo = ft.Text('',color=Colors.BLACK)
    titulo_book_para_emprestimo = ft.Text('',color=Colors.BLACK)
    isbn_book_para_emprestimo = ft.Text('',color=Colors.BLACK)
    def realizar_emprestimo(book):
        if not book['status']:
            page.go('/biblioteca')
            page.overlay.append(msg_error_emprestimo)
            msg_error_emprestimo.open = True
            return page.update()
        dados = get_usuarios()
        campo_user_post_emprestimo.options = [
            ft.dropdown.Option(text=user['nome'], key=user['id']) for user in dados
        ]

        id_book_para_emprestimo.value = book['id do livro']
        titulo_book_para_emprestimo.value = book['titulo']
        isbn_book_para_emprestimo.value = book['ISBN']
        # ft.Text(value=book['id_livro'])
        # ft.Text(value=book['titulo'])
        # ft.Button(text='Realizar Emprstimo',on_click=lambda _, u=book: executar_emprestimo(u))
        return page.go('/realizar_emprestimo')

    def executar_emprestimo(e):
        dados = post_emprestimo(campo_user_post_emprestimo.value,isbn_book_para_emprestimo.value)
        if 'error' in dados:

            abu = ft.Text(value='usuario não selecionado')
            snack_personalizado = ft.SnackBar(content=abu, bgcolor=Colors.RED, duration=2000)
            page.overlay.append(snack_personalizado)
            snack_personalizado.open = True
            page.update()

        else:
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()
            page.go('/biblioteca')
        # dados = post_emprestimo(1, book['ISBN'])
        # if 'error' in dados:
        #     abu = ft.Text(value=dados['error'])
        #     snack_personalizado = ft.SnackBar(content=abu, bgcolor=Colors.RED, duration=2000)
        #     page.overlay.append(snack_personalizado)
        #     snack_personalizado.open = True
        #     return page.update()




    # a = ft.Text(value='teste1')
    # b = ft.Text(value='teste2')
    # c.append(a)
    # c.append(b)

    campo_user_post_emprestimo = ft.Dropdown(
        label='Usuarios',)
    def salvar_atualizacao(e):
        if campo_nome.value == '' or campo_cpf.value == '' or campo_endereco.value == '':
            page.overlay.append(msg_errror_vazios)
            msg_errror_vazios.open = True
            return page.update()
        dados = put_usuario(int(campo_id.value), campo_nome.value, campo_cpf.value, campo_endereco.value)
        if 'error' in dados:
            abu = ft.Text(value=dados['error'])
            snack_personalizado = ft.SnackBar(content=abu, bgcolor=Colors.RED, duration=2000)
            page.overlay.append(snack_personalizado)
            snack_personalizado.open = True
            return page.update()
        page.overlay.append(msg_sucesso)
        msg_sucesso.open = True
        page.go('/usuarios')
        page.update()

    def salvar_editar_livro(e):
        dados = put_livro(int(campo_id_livro.value), campo_titulo.value,
                          campo_autor.value, campo_resumo.value, campo_ISBN.value)
        if 'error' in dados:
            abu = ft.Text(value=dados['error'])
            snack_personalizado = ft.SnackBar(content=abu, bgcolor=Colors.RED, duration=2000)
            page.overlay.append(snack_personalizado)
            snack_personalizado.open = True
            return page.update()
        page.overlay.append(msg_sucesso)
        msg_sucesso.open = True
        page.go('/biblioteca')
        page.update()

    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)


    # Componentes////////////////////////////////////////////////////////////////////////////////////////////////

    id_emprestimo = ft.Text('',color='#153147')
    data_emprestimo = ft.Text('',color='#153147')
    data_de_devolucao = ft.Text('',color='#153147')
    emprestimo_usuario_id = ft.Text('',color='#153147')
    emprestimo_usuario_nome = ft.Text('',color='#153147')
    emprestimo_usuario_CPF = ft.Text('',color='#153147')
    emprestimo_usuario_endereco = ft.Text('',color='#153147')
    emprestimo_livro_isbn = ft.Text('',color='#153147')
    emprestimo_livro_titulo = ft.Text('',color='#153147')
    emprestimo_livro_status = ft.Text('',color='#153147')


    campo_user_id = Text('Nome do livro: ', color='#153147')
    campo_user_nome = TextField(label='Nome completo: ', color="#C8D9E6",selection_color="#153147",
                                border_color="#C8D9E6",focused_border_color=Colors.WHITE,bgcolor="#153147",
                                border_width=3,border_radius=7)
    campo_user_CPF = TextField(label='CPF do usuario: ', color="#C8D9E6",selection_color="#153147",
                               border_color="#C8D9E6",focused_border_color=Colors.WHITE,bgcolor="#153147",
                               border_width=3,border_radius=7)
    campo_user_endereco = TextField(label='Endereço: ', color="#C8D9E6",selection_color="#153147",
                                    border_color="#C8D9E6",focused_border_color=Colors.WHITE,bgcolor="#153147",
                                    border_width=3,border_radius=7)


    campo_book_titulo = TextField(label='Nome do livro: ', color="#C8D9E6",selection_color="#153147",border_color="#C8D9E6",focused_border_color=Colors.WHITE,bgcolor="#153147",border_width=3,border_radius=7)
    campo_book_autor = TextField(label='Autor da obra', color="#C8D9E6",selection_color="#153147",border_color="#C8D9E6",focused_border_color=Colors.WHITE,bgcolor="#153147",border_width=3,border_radius=7)
    campo_book_resumo = TextField(label='Resumo do Livro', color="#C8D9E6",selection_color="#153147",border_color="#C8D9E6",focused_border_color=Colors.WHITE,bgcolor="#153147",border_width=3,border_radius=7)
    campo_book_ISBN = TextField(label='Código unico ISBN', color="#C8D9E6",selection_color="#153147",border_color="#C8D9E6",focused_border_color=Colors.WHITE,bgcolor="#153147",border_width=3,border_radius=7)

    campo_id_livro = Text('', color='#153147')
    campo_titulo = TextField('', color='#153147')
    campo_autor = TextField('', color='#153147')
    campo_resumo = TextField('', color='#153147')
    campo_ISBN = TextField('', color='#153147')

    nome_usuario = ft.Text('')
    cpf_usuario = ft.Text('')
    endereco_usuario = ft.Text('')

    appbar_text_ref = ft.Ref[ft.Text]()

    def handle_menu_item_click(e):
        page.go("/cadastrar_livro")
        print(f"{e.control.content.value}.on_click")
        page.open(
            ft.SnackBar(content=ft.Text(f"pagina de {e.control.content.value}",color=Colors.WHITE),bgcolor="#153147",duration=500)
        )
        appbar_text_ref.current.value = e.control.content.value
        page.update()

    def handle_menu_usuario(e):
        page.go("/cadastrar_usuario")
        print(f"{e.control.content.value}.on_click")
        page.open(
            ft.SnackBar(content=ft.Text(f"pagina de {e.control.content.value}",color=Colors.WHITE),bgcolor="#153147",duration=500)
        )
        appbar_text_ref.current.value = e.control.content.value
        page.update()

    def handle_menu_emprestimos(e):
        page.go("/emprestimos")
        print(f"{e.control.content.value}.on_click")
        page.open(
            ft.SnackBar(content=ft.Text(f"pagina de {e.control.content.value}",color=Colors.WHITE),bgcolor="#153147",duration=500)
        )
        appbar_text_ref.current.value = e.control.content.value
        page.update()

    def handle_submenu_open(e):
        print(f"{e.control.content.value}.on_open")

    def handle_submenu_close(e):
        print(f"{e.control.content.value}.on_close")

    def handle_submenu_hover(e):
        print(f"{e.control.content.value}.on_hover")

    page.appbar = ft.AppBar(
        title=ft.Text("Menus", ref=appbar_text_ref),
        center_title=True,
        bgcolor=ft.Colors.BLUE,
    )
    opcoes = ft.PopupMenuButton(
                        icon=ft.Icons.MORE_HORIZ_OUTLINED, icon_color=Colors.BLACK,
                        items=[
                            # ft.PopupMenuItem(text='Biblioteca', on_click=lambda _: page.go('/biblioteca')),
                            ft.PopupMenuItem(text='Cadastrar livro', on_click=lambda _: page.go('/cadastrar_livro')),
                            # ft.PopupMenuItem(text='Cadastrar emprestimo', on_click=lambda _: page.go('/realizar_emprestimo')),
                            ft.PopupMenuItem(text='Cadastrar_usuario', on_click=lambda _: page.go('/cadastrar_usuario')),
                            ft.PopupMenuItem(text='Exibir usuarios', on_click=lambda _: page.go('/usuarios')),
                            ft.PopupMenuItem(text='Exibir emprestimo', on_click=lambda _: page.go('/emprestimos')),
                        ],bgcolor="#0000000"
                    )
    menubar = ft.MenuBar(
        expand=True,
        style=ft.MenuStyle(
            alignment=ft.alignment.top_right,
            bgcolor="#153147",
            mouse_cursor={
                ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
            },
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Biblioteca"),
                width=250,
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.Column(
                        [
                            ft.MenuItemButton(
                                content=ft.Text("Cadastrar Livro",size=10),
                                leading=ft.Icon(ft.Icons.BOOK),
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: "#5a1f13"}
                                ),
                                on_click=handle_menu_item_click,
                            ),

                            ft.MenuItemButton(
                                content=ft.Text("Cadastrar Usuario",size=10),
                                leading=ft.Icon(ft.Icons.PERSON),
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: "#5a1f13"}
                                ),
                                on_click=handle_menu_usuario,
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Emprestimos",size=10),
                                leading=ft.Icon(ft.Icons.TIMER),
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: "#5a1f13"}
                                ),
                                on_click=handle_menu_emprestimos,
                            ),


                        ]
                    ),

                ],
            ),

        ],
    )



    msg_sucesso = ft.SnackBar(
        content=ft.Text(value='nome salvado com sucesso'),
        bgcolor=Colors.GREEN,
        duration=1000,
    )

    msg_error = ft.SnackBar(
        content=ft.Text(value='O cpf já foi registrado em outro usuario'),
        bgcolor=Colors.RED,
        duration=2000,
    )
    msg_error_repetido = ft.SnackBar(
        content=ft.Text(value='nome repetido'),
        bgcolor=Colors.RED,
        duration=2000,
    )
    lv_Descricao = ft.ListView(
        height=500,
    )

    logo = ft.GestureDetector(
        on_tap=lambda e: page.go("/"),  # substitua "/inicio" pela rota que quiser
        content=ft.Image(
            src="logobiblioteca-removebg-preview.png",  # troque para o caminho da sua imagem local ou URL
            width=40,
            height=40,
            color=Colors.WHITE,
            fit=ft.ImageFit.CONTAIN
        )
    )

    logo2 = ft.Image(
        src="logobiblioteca-removebg-preview.png",
    )
    # perfil = ft.PopupMenuButton(
    #                     icon=ft.Icons.PERSON,
    #                     items=[
    #                         ft.PopupMenuItem(text='detalhes',on_click=lambda _: page.go('/terceira')),
    #                     ]
    #                 )
    perfil = ft.IconButton(
        icon=ft.Icons.PERSON,
        on_click=lambda _: page.go('/usuarios'),
    )
    livro = ft.IconButton(
        icon=ft.Icons.BOOK,
        on_click=lambda _: page.go('/biblioteca'),
    )

    nome_usuario = ft.Text('', color=Colors.BLACK)
    cpf_usuario = ft.Text('', color=Colors.BLACK)
    endereco_usuario = ft.Text('', color=Colors.BLACK)


    input_nome = ft.TextField(label="Digite o nome do livro")
    input_descricao = ft.TextField(label='insira a descricao do livro')
    input_autor = ft.TextField(label='insira o autor do livro')
    input_categoria = ft.TextField(label='insira a categoria do livro')
    input_isbn = ft.TextField(label='insira o ISBN do livro')
    input_resumo = ft.TextField(label='insira o resumo do livro')

    txt_titulo = ft.Text('')
    txt_autor = ft.Text('')
    txt_descricao = ft.Text('')
    txt_categoria = ft.Text('')
    txt_ISBN = ft.Text('')
    # Eventos
    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar

    page.go(page.route)

# Comando que executa o aplicativo
# Deve estar sempre colado na linha
ft.app(main)