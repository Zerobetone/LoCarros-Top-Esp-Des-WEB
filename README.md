# LOCarros

Disciplina: Tópicos Especiais em Desenvolvimento Web (8° semestre)

Curso: Ciência da Computação - Instituto Federal de Educação, Ciência e Tecnologia do Ceará (IFCE)

O [LOCarros](https://github.com/Zerobetone/LoCarros-Top-Esp-Des-WEB) é sistema simples para o controle de locação de veículos desenvolvido com Bootstrap e Django.

## Equipe

* [Bruno Brito](https://github.com/Brunostd)
* [José Roberto](https://github.com/Zerobetone)
* [Lucas Araújo](https://github.com/lucapwn)
* [Maria Madalena](https://github.com/Maria-collab)

## Tecnologias

* HTML, CSS e JavaScript
* Bootstrap
* Git e GitHub
* Python e Django
* Banco de dados SQLite

## Branches

* [Front-End](https://github.com/Zerobetone/LoCarros-Top-Esp-Des-WEB)
* [Back-End](https://github.com/Zerobetone/LoCarros-Top-Esp-Des-WEB/tree/back-end)
* [Diagrama de Classes](https://github.com/Zerobetone/LoCarros-Top-Esp-Des-WEB/tree/Diagram)

## Executando o sistema
### Clone o repositório
~~~shell
git clone https://github.com/Zerobetone/LoCarros-Top-Esp-Des-WEB.git
~~~
### Instale as dependências
~~~shell
pip install -r requirements.txt
~~~
### Aplique as modificações no banco de dados
~~~shell
python manage.py migrate
~~~
### Execute o sistema
~~~shell
python manage.py runserver
~~~

Navegue até [http://127.0.0.1:8000](http://127.0.0.1:8000)

**O usuário e a senha do [painel administrativo](http://127.0.0.1:8000/admin) é ```admin```**.

(Será adicionado mais detalhes após a conclusão do sistema)
