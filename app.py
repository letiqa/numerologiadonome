
from flask import Flask, render_template, request
import unicodedata
import mimetypes

mimetypes.add_type('font/otf', '.otf')

app = Flask(__name__) 

TABELA_PITAGORICA = {
    "A": 1, "J": 1, "S": 1,
    "B": 2, "K": 2, "T": 2,
    "C": 3, "L": 3, "U": 3,
    "D": 4, "M": 4, "V": 4,
    "E": 5, "N": 5, "W": 5,
    "F": 6, "O": 6, "X": 6,
    "G": 7, "P": 7, "Y": 7,
    "H": 8, "Q": 8, "Z": 8,
    "I": 9, "R": 9,
}

SIGNIFICADOS = {
    1: "É o Líder. Você veio para exercer a liderança e atrair seguidores. Tem o pensamento autocentrado. Com confiança e criatividade  pode alcançar grandes vitórias.\n\nAspectos Construtivos: Atividade, pioneirismo, independência, invenção, força, ambição\n\nPossíveis Aspectos Densos: Preguiça, egoísmo, dominação, rivalidade.",
    2: "Parceiro e diplomata, coopera e pacifica ambientes. Tem sensibilidade e facilidade em lidar com situações tensas.\nTrabalha bem em equipe e resolvendo conflitos, o que pode trazer certo desgaste.\n\nAspectos positivos: Harmonia, diplomacia, consideração, atenção aos detalhes, paciência.\n\nPossíveis aspectos negativos: supersensibilidade, negligência, dependência, covardia, crueldade.",
    3: "É o Comunicador, e veio para espalhar alegria. Será bom em qualquer profissão que use a imaginação e a autoexpressão. \nDeve buscar o autoconhecimento. Cuidado ao assumir muitas responsabilidades, pode não dar conta. \n\nAspectos Construtivos: alegria, otimismo, comunicação. \n\nPossíveis aspectos negativos: pessimismo, extravagância, hipocrisia.",
    4: "Veio para construir, solidificar e inspirar confiança. Muito prático e organizado, em especial com finanças. É uma pessoa trabalhadora, sistemática e estável. \nO sucesso virá, mas não da noite para o dia. Deve fazer a sua parte, e permitir que o universo faça a dele. \n\nAspectos Construtivos: confiabilidade, determinação, honestidade, lealdade, organização, economia.\n\nPossíveis aspectos negativos: rigidez, impaciência, autoritarismo, desorganização, crueldade, ciúme.",
    5: "Espírito Livre, traz mudança e quebra paradigmas. Tem habilidades de compreensão do que é abstrato e dom com palavras.\nLembre-se que liberdade é diferente de rebeldia.\n\nAspectos construtivos: liberdade, aventura, ousadia, progresso, versatilidade.\n\nPossíveis aspectos negativos: irresponsabilidade, falta de comprometimento, deboche, vícios.",
    6: "Se dedica ao ambiente familiar e à comunidade. Tem capacidade de assumir grandes responsabilidades. Profissões ligadas ao cuidado são indicações de sucesso. \nÉ importante cuidar com a tendência de querer cuidar de todo mundo e esquecer de si mesmo.\n\nAspectos Construtivos: Serviço, responsabilidade, domesticidade, bondade.\n\nPossíveis aspectos negativos: preocupação, intromissão, carência, ciúme, presunção, chantagem.",
    7: "Pensador e curioso, analisa tudo com cautela. Sua intuição é aguçada, com capacidade analítica.Sua mente procura encontrar as respostas para questões profundas da vida. \nBusque adquirir sabedoria, de forma neutra, para que não se torne um fanático e viva com humildade.\n\nAspectos construtivos: introspecção, silêncio, sensatez, estudioso.\n\nPossíveis aspectos negativos: sarcasmo, frieza, melancolia, egocentrismo, manipulação.",
    8: "Realizador, busca o sucesso por seus próprios esforços. Trabalha sempre em prol de um bem maior e não só pelo dinheiro. Terá grandes oportunidades que dependem do seu esforço em equilibrar a vida material e espiritual. O 8 é o número da justiça e você sempre será guiado por ela. Será excelente em tudo o que se determinar a fazer.\n\nAspectos positivos: desapego, esforço, coragem, liderança.\n\nPossíveis aspectos negativos: impaciência, crueldade, injustiça, falsidade, vícios.",
    9: "Generoso, aconselha com sabedoria e sabe respeitar as diferenças. Sua compaixão faz com que saiba se colocar no lugar do outro como ninguém. Busque o perdão e também o autoconhecimento. A sua armadilha é tornar-se obsoleto e apegado ao passado. \nLembre-se que só conseguimos ajudar verdadeiramente as pessoas quando nos ajudarmos primeiro.\n\nAspectos Positivos: altruísmo, generosidade, amor universal, serviço, simpatia.\n\nPossíveis aspectos negativos: egoísmo, emotivo, amargura, falsidade, vícios.",
    11: "Líder Servidor, aquele que abre caminhos. Nunca reduzimos o 11 a 2, pois o 11 é líder, o 2 é o cooperador. Porém por ser uma vibração de número mestre, tem a habilidade de ser líder e ao mesmo tempo cooperador. É provável que passe desafios, principalmente em relação a cobrança das pessoas. Não se cobre tanto, seu campo magnético é de muita luz e isso atrai sombras. Tem o dom da profecia. \nEm alguns momentos poderá se sentir sobrecarregado e pode viver todas as negatividades do número 2 (leia as observações desse número), lembre-se que poderá escolher o que deseja viver. \n\nAspectos construtivos: Intuição, fé, inspiração, invenção, revelação, idealismo. \n\nPossíveis aspectos negativos: fanatismo, falta de objetivos, carência, medo, desonestidade, avareza, perversidade.",
    22: "Mestre Construtor, veio para liderar e assumir grandes responsabilidades. Busca o poder e a fortuna, e se sua intenção for de melhorar a vida das pessoas, obterá sucesso. Tem capacidade política, será recompensado na medida em que servir com ética. \nPode acabar vivendo as negatividades do número 4 (leia as observações desse número), limitando sua potencialidade. Seja quem você nasceu para ser e não desperdice seus talentos. \n\nAspectos construtivos: poder, liderança, influência, praticidade, expansão. \n\nPossíveis aspectos negativos: indiferença, complexo de inferioridade, reprovação, perversidade, imprudência, incapacidade, manipulação.",
    33: "",
}

NUMEROS_VALIDOS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33)

@app.route("/", methods=["GET", "POST"])
def homepage():
    numero = None
    significado = None
    nome = None

    if request.method == "POST":
        nome = request.form["nome"]
    
        nome_sem_acento = unicodedata.normalize("NFKD", nome).encode("ASCII", "ignore").decode("ASCII")
        nome_normalizado = nome_sem_acento.upper().replace(" ", "")

        resultado_bruto = sum(TABELA_PITAGORICA[letra] for letra in nome_normalizado)

        #entender melhor a função
        numero_do_nome = resultado_bruto

        while numero_do_nome not in NUMEROS_VALIDOS:
              numero_do_nome = sum(int(digito) for digito in str(numero_do_nome))

        significado = SIGNIFICADOS[numero_do_nome]
        numero = numero_do_nome

    

    return render_template(
        "index.html",
        nome=nome,
        numero=numero,
        significado=significado
    )

if __name__ == "__main__":
    app.run(debug=True)
