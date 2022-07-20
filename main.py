# Author: Lucas Burle

import random
import re
import matplotlib.pyplot as plt


def simulate_choices(n, readers):
    output = ""

    for i in range(0, n):
        output = output + "#### EXPERIMENTO " + str(i+1) + " ####\n"

        for reader in readers:
            reader_choice = random.choices([book[0] for book in reader.booksProbability], weights=[book[1] for book in reader.booksProbability], k=1)
            reader_choice_output = "Leitor " + str(reader.id) + " escolheu " + str(reader_choice.pop())
            output = output + reader_choice_output + "\n"

        output = output + "\n"

    with open("output.txt", "w+") as output_file:
        output_file.write(output)


def int_input(msg, interval=(0, 0), special_choice=False):
    while True:
        try:
            user_input = int(input(msg))

            if special_choice and user_input == -1:
                break

            if interval[0] < interval[1]:
                if not (interval[0] <= user_input <= interval[1]):
                    raise ValueError()

            break
        except ValueError:
            print("Entrada inválida.\n")

    return user_input


def generate_histogram_data(readers, books):
    histogram_data = {reader: {book: 0 for book in books} for reader in readers}

    with open("output.txt") as output_file:
        lines = output_file.readlines()

        for line in lines:
            if "Leitor" in line:
                pattern = '^Leitor\\s(\\d+) escolheu\\s.*?(\\d+)'
                regex_match = re.match(pattern, line)
                reader_id = int(regex_match.group(1))
                book_id = int(regex_match.group(2))

                book = next((book for book in books if book.id == book_id), None)
                reader = next((reader for reader in readers if reader.id == reader_id), None)

                histogram_data[reader][book] += 1

    return histogram_data


def generate_histogram(readers, books, reader_id):
    histogram_data = generate_histogram_data(readers, books)
    reader = next((reader for reader in readers if reader.id == reader_id), None)
    book_count = list()

    if reader_id == -1:
        for _, f_dict in histogram_data.items():
            for book, frequency in f_dict.items():
                book_count = book_count + [book.id for i in range(0, frequency)]
    else:
        for book, frequency in histogram_data[reader].items():
            book_count = book_count + [book.id for i in range(0, frequency)]

    plt.hist(book_count, bins=len(books))

    plt.xlabel("Livro")
    plt.ylabel("Frequência de escolha")
    plt.margins(0)
    plt.xticks(range(0, len(books)+1, 1))

    plt.show()


class Book:

    id = 1

    def __init__(self, title):
        self.title = title
        self.id = Book.id

        Book.id += 1

    def __str__(self):
        return self.title + " (" + str(self.id) + ")"


class Reader:

    id = 1

    # booksProbability é uma tupla do tipo (book:Book, probabilidade:float[0, 1])
    def __init__(self, books):
        self.booksProbability = self.generate_probabilities(books)
        self.id = Reader.id
        Reader.id += 1

    @classmethod
    def generate_probabilities(cls, books):
        probabilities = [(book, random.randint(0, 100)) for book in books]  # Gera lista de tuplas do tipo (livro, probabilidade de escolha)
        weight_sum = sum(prob[1] for prob in probabilities)  # Soma todas as probabilidades de escolha da lista.
        probabilities = list(map(lambda book: (book[0], book[1]/weight_sum), probabilities))  # Normaliza as probabilidades para estarem contidas entre 0 e 1.

        return probabilities

    def __str__(self):
        return ",".join(["(" + str(book[0]) + "," + str(book[1]) + ")" for book in self.booksProbability])


def pairing_frequency(n_simulations):
    pairing_count = 0
    experiment_dict = extract_experiments(n_simulations)

    for _, books_ids in experiment_dict.items():
        previous_book_id = -1

        for idx, book_id in enumerate(books_ids):
            if previous_book_id == book_id:
                break

            if idx == (len(books_ids) - 1):  # É o último id da lista.
                pairing_count += 1

            previous_book_id = book_id

    return pairing_count/n_simulations


def all_repeated_frequency(n_simulations):
    repeat_count = 0
    experiment_dict = extract_experiments(n_simulations)

    for _, books_ids in experiment_dict.items():
        previous_book_id = books_ids[0]

        for idx, book_id in enumerate(books_ids):
            if previous_book_id != book_id:
                break

            if idx == (len(books_ids) - 1):  # É o último id da lista.
                repeat_count += 1

            previous_book_id = book_id

    return repeat_count/n_simulations


def extract_experiments(n_simulations):
    experiment_dict = {}

    with open("output.txt") as output_file:
        lines = output_file.readlines()

        for line in lines:
            if "EXPERIMENTO" in line:
                simulation_id = re.match('^####\\sEXPERIMENTO\\s(\\d+)', line).group(1)
                choosed_books = list()

            elif "Leitor" in line:
                book_id = int(re.match('.*?escolheu\\s.*?(\\d+)', line).group(1))
                choosed_books.append(book_id)

            elif line == "\n":
                experiment_dict[simulation_id] = choosed_books

    return experiment_dict


if __name__ == '__main__':
    with open('book_titles.txt') as book_titles_file:
        books = [Book(title.strip()) for title in book_titles_file.readlines()]

    print("Esta biblioteca de livros raros possui K usuarios e M livros.")
    print("Adicione novos livros modificando o arquivo 'book_titles.txt' na raiz do projeto. Siga o padrão do arquivo, não deixe linhas em branco.")
    print("Você pode usar este site https://www.fantasynamegenerators.com/book-title-generator.php para gerar títulos.")

    nReaders = int_input("Digite um número inteiro para a quantidade de leitores que deseja simular: ")
    readers = [Reader(books) for i in range(0, nReaders)]

    menu_choice = -1
    user_choice = -1
    print('\n' * 20)
    while menu_choice != 0:

        print("Digite 1 para imprimir as probabilidades de escolha de todos leitores")
        print("Digite 2 para simular o experimento aleatório da escolha dos leitores")
        print("Digite 3 para entrar no menu de frequências")
        print("Digite 0 para fechar o programa")

        menu_choice = int_input("Digite sua escolha: ")
        print("\n")

        if menu_choice == 1:
            for reader in readers:
                print("[" + str(reader) + "]" + "\n")
            input("Digite enter para continuar...")

        elif menu_choice == 2:
            n_simulations = int_input("Digite um número inteiro para a quantidade de vezes que deseja simular o experimento: ")
            simulate_choices(n_simulations, readers)

        elif menu_choice == 3:
            print("\n" * 5)

            while True:
                print("\n\n")
                print("Digite 1 para gerar o histograma de escolhas.")
                print("Digite 2 para gerar a frequência relativa de emparelhamentos.")
                print("Digite 3 para gerar a frequência relativa dos eventos nos quais todos os leitores escolhem o mesmo livro.")
                print("Digite 0 para sair do menu de frequências.")
                menu_choice = int_input("Digite sua escolha: ", interval=(0, 3))
                print("\n\n")
                if menu_choice == 1:
                    user_choice = int_input("Digite um número inteiro no intervalo [1, " + str(nReaders) + "] para escolher o leitor que deseja gerar o histograma, ou digite -1 para agrupar todos os leitores: ", interval=(1, nReaders), special_choice=True)
                    generate_histogram(readers, books, user_choice)

                elif menu_choice == 2:
                    print("A frequência relativa de emparelhamentos é: " + str(pairing_frequency(n_simulations)))

                elif menu_choice == 3:
                    print("A frequência relativa dos nos quais todos os leitores escolhem o mesmo livro é: " + str(all_repeated_frequency(n_simulations)))

                elif menu_choice == 0:
                    menu_choice = -1
                    break

        print('\n' * 20)
