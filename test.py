import forecast

def main():
    fc = forecast.ForecastClient('c11578a4-fb00-43dd-b3ec-bf55df3a1a38')

    task = fc.tasks.from_company_id(3968)
    print(task)

main()