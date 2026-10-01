import random

def is_prime_number(n: int) -> bool:
    """Verifica se um número inteiro é primo.

    Um número primo é um inteiro maior que 1 que possui exatamente 2 divisores
    positivos: 1 e ele mesmo.

    Args:
        n (int): O número inteiro a ser testado.

    Returns:
        bool: True se `n` for primo, False caso contrário.

    Exemplos:
        >>> is_prime_number(2)
        True
        >>> is_prime_number(4)
        False
        >>> is_prime_number(17)
        True
    """
    if n < 2:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    f = 3

    while f * f <= n:
        if n % f == 0:
            return False
        f += 2

    return True


def generate_prime(min_value: int, max_value: int) -> int:
    """Gera um número primo aleatório dentro de um intervalo inclusivo.

    Utiliza uma abordagem de amostragem por rejeição (*Monte Carlo*), sorteando
    inteiros aleatórios no intervalo [min_value, max_value] até encontrar um
    número que satisfaça o teste de primalidade `is_prime_number`.

    Args:
        min_value (int): O menor valor possível do intervalo (inclusivo).
        max_value (int): O maior valor possível do intervalo (inclusivo).

    Returns:
        int: Um número primo pertencente ao intervalo [min_value, max_value].

    Exemplos:
        >>> random.seed(42)
        >>> generate_prime(10, 50)
        13
    """
    while True:
        n = random.randint(min_value, max_value)

        if is_prime_number(n):
            return n

def mdc(a: int, b: int) -> int:
    """Calcula o Máximo Divisor Comum (MDC) entre dois números inteiros.

    Aplica o Algoritmo de Euclides por divisões sucessivas, fundamentado na
    propriedade de que o MDC entre dois números também divide perfeitamente
    o resto da divisão entre eles: mdc(a, b) = mdc(b, a mod b).

    Args:
        a (int): O primeiro número inteiro.
        b (int): O segundo número inteiro.

    Returns:
        int: O maior divisor comum entre `a` e `b`.

    Exemplos:
        >>> mdc(48, 18)
        6
        >>> mdc(101, 10)
        1
        >>> mdc(0, 5)
        5
    """
    while b != 0:
        a, b = b, a % b

    return a


def mod_inverse(a: int, m: int) -> int:
    """Encontra o inverso multiplicativo modular de 'a' módulo 'm'.

    Busca um valor inteiro d tal que a congruência (d * a) % m == 1 seja
    satisfeita.

    Args:
        a (int): O número para o qual se busca o inverso modular.
        m (int): O módulo da operação (deve ser maior que 1).

    Returns:
        int: O menor inteiro positivo d no intervalo [1, m - 1] tal que
        (d * a) % m == 1.

    Raises:
        ValueError: Se o inverso modular não existir (ou seja, quando a e m não
          forem primos entre si).

    Exemplos:
        >>> mod_inverse(3, 11)
        4
        >>> mod_inverse(10, 17)
        12
    """
    for d in range(1, m):
        if (d * a) % m == 1:
            return d

    raise ValueError("Não existe inverso modular")


def encrypt(key: tuple[int, int], msg: str) -> str:
    """
    key = (e, n)

    A mensagem é convertida para UTF-8 e dividida
    em blocos de 3 bytes.

    Cada bloco é convertido para um número e então
    cifrado usando:

        c = m^e mod n
    """

    e, n = key

    data = msg.encode("utf-8")

    blocks = []

    for i in range(0, len(data), 3):
        block_bytes = data[i:i + 3]

        block = 0

        for byte in block_bytes:
            block = (block << 8) | byte

        blocks.append(block)

    encrypted = []

    for block in blocks:
        if block >= n:
            raise ValueError("Bloco maior ou igual ao módulo RSA")

        c = pow(block, e, n)
        encrypted.append(str(c))

    return " ".join(encrypted)

def decrypt(key: tuple[int, int], msg: str) -> str:
    """
    key = (d, n)

    Cada valor cifrado é transformado usando:

        m = c^d mod n

    Cada bloco recuperado é então convertido novamente
    para seus bytes originais.
    """

    d, n = key

    decrypted = bytearray()

    for value in msg.split():
        c = int(value)

        # RSA
        block = pow(c, d, n)

        # Converte o número de volta para 3 bytes
        decrypted.extend(block.to_bytes(3, byteorder="big"))

    return bytes(decrypted).decode("utf-8")

def generate_rsa_key_pair() -> tuple[tuple[int, int], tuple[int, int]]:
    """Gera um par de chaves RSA (pública e privada) para fins didáticos.

    Sorteia dois números primos distintos 'p' e 'q', calcula o módulo RSA 'n' e a
    função totiente de Euler 'phi', determina o expoente público 'e' e obtém
    o expoente privado 'd'.

    Returns:
        tuple[tuple[int, int], tuple[int, int]]: Uma tupla contendo duas
        sub-tuplas:
            - public_key (tuple[int, int]): A chave pública na forma (e, n).
            - private_key (tuple[int, int]): A chave privada na forma (d, n).

    Exemplos:
        >>> pub_key, priv_key = generate_rsa_key_pair()
        >>> print(pub_key)
        (3, 31834927)
        >>> print(priv_key)
        (21217827, 31834927)
    """
    while True:
        p = generate_prime(5000, 10000)
        q = generate_prime(5000, 10000)

        if p == q:
            continue

        n = p * q

        # Blocos de 3 bytes precisam caber em n
        if n > 0xFFFFFF:
            break

    phi = (p - 1) * (q - 1)

    e = 2

    while e < phi:
        if mdc(e, phi) == 1:
            break
        e += 1

    d = mod_inverse(e, phi)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key

def key_to_string(key: tuple[int, int]) -> str:
    return f"{key[0]},{key[1]}"

def string_to_key(key: str) -> tuple[int, int]:
    splitted_key = key.split(",")
    return (int(splitted_key[0]), int(splitted_key[1]))
