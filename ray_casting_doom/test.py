response_tests = [
        {
            "description": "belyuga_about",
            "id": 118,
            "key": "test_belyuga"
        },
        {
            "description": "New sellers initial launch",
            "id": 9,
            "key": "NewSellerTest"
        },
]
ab_test_from_db = [
        {
            "created_at": "datetime.datetime(2020, 12, 23, 16, 16, 20, 326847, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800)))",
            "description": "test",
            "id": 1,
            "key": "test1",
            "updated_at": "datetime.datetime(2020, 12, 23, 16, 16, 20, 326847, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800)))",
            "updated_by": 'null'
        },
]


list_dict = [
    {'id': 3, 'a': 'lol'},
    {'id': 2, 'a': 'kek'},
    {'id': 1, 'a': 'cheburek'},
]

def sort_list_of_dict(list, key):
    """
    Сортировка списка(массива), содержащего внутри словари, по значению словаря
    :param list: Массив, соддержаший словари
    :param key: Ключ словаря, по которому небходио отсортировать массив
    :return: Возвращает отсортированный массив
    """
    return sorted(list, key=lambda i: dict(i)[key])


for test_from_response, test_from_db in zip(response_tests, ab_test_from_db):
    print( test_from_response['id'], test_from_db['id'])

pass

# assert len(response.tests) == len(ab_test_from_db)
# ab_test_from_db_sorted = sort_list_of_dict(ab_test_from_db, 'id')
# response_sorted = sort_list_of_dict(response.tests, 'id')

