# API5BD2026Backend
Repository for the implementation of an academic project in partnership with a real company. API5 2026.1 Fatec SJC/SP.
WARJ-10: Adicionado Sprint-1 para inicialiação do projeto.


[Databases](database/Db.md)

Alterações em readme!

1. Ruff: Linter e Imports (Achar erros lógicos)
   Ele vai procurar variáveis que você criou e não usou, imports duplicados, erros de sintaxe, etc.

Para apenas verificar: ruff check .

Para corrigir automaticamente (Recomendado): ruff check --fix .

2. Ruff: Formatador (Deixar o código bonito)
   Ele vai arrumar os espaços, quebras de linha e aspas para ficarem no padrão oficial.

Para apenas verificar (igual o CI faz): ruff format --check .

3. Mypy: Checagem de Tipos
Ele vai ler o seu código procurando erros de tipagem (ex: você disse que a função recebia um int, mas está passando uma string). O Mypy não corrige sozinho, ele apenas avisa onde você precisa arrumar.

Para verificar: mypy .

Para formatar automaticamente (Recomendado): ruff format .