import pandas as pd
from dateutil.parser import parse
import math
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring


def extract():
    pizza_types = pd.read_csv('pizza_types.csv', encoding='latin1')
    orders = pd.read_csv('orders.csv', encoding='latin1')
    order_details = pd.read_csv(
        'order_details.csv', encoding='latin1')
    pizzas = pd.read_csv(
        'pizzas.csv', encoding='latin1')
    return pizza_types, orders, order_details, pizzas


def transform(pizza_types, orders, order_details):
    orders.pop('time')  # Al final del dia son datos que no me interesan
    # Ya tengo esto ordenado y parseado.
    orders['date'] = pd.to_datetime(pd.Series((orders['date'].apply(parse))))
    orders['date'] = orders['date'].apply(
        lambda x: x.week % 53)  # Indicamos la semana
    return orders, order_details, pizza_types


def get_ingredients(pizza_types):
    ingredientes_por_pizza = {}
    # Va a contener el numero total de ingredientes por semana.
    ingredientes = {}
    for i in range(len(pizza_types)):
        aux = pizza_types.ingredients[i].split(',')
        ingredientes_por_pizza[pizza_types.pizza_type_id[i]] = [
            i.strip() for i in aux]
        for j in aux:
            if j not in ingredientes:
                ingredientes[j.strip()] = [0 for i in range(53)]
    return ingredientes, ingredientes_por_pizza


def sum_ingredients(pizza, ingredientes, ingredientes_por_pizza, semana, cantidad):
    tamaños = {'s': 1, 'm': 1.4, 'l': 1.8}
    if pizza not in ingredientes_por_pizza:
        suma = tamaños[pizza[-1]]
        if pizza[len(pizza)-2:] == 'xl':  # Este es el caso particular de The greek
            if pizza[-3] == 'x':
                pizza = pizza[:-4]
                suma = 2.2
            else:
                pizza = pizza[:-3]
                suma = 2.8
        else:
            pizza = pizza[:-2]
    else:
        suma = 1.4
    pizza = pizza.strip()
    for h in ingredientes_por_pizza[pizza]:
        ingredientes[h][semana] += cantidad*suma
    return ingredientes


def get_ingredients_per_week(orders, order_details, pizza_types):
    ingredientes, ingredientes_por_pizza = get_ingredients(pizza_types)
    for i in range(len(order_details)):
        info = order_details.loc[i]
        semana = list(orders[orders.order_id == info['order_id']]['date'])[0]
        pizza = info['pizza_id']
        cantidad = info['quantity']
        ingredientes = sum_ingredients(
            pizza, ingredientes, ingredientes_por_pizza, semana, cantidad)
    return convert_int(ingredientes)


def convert_int(ingredientes):
    for i in ingredientes:
        for j in range(len(ingredientes[i])):
            ingredientes[i][j] = math.ceil(ingredientes[i][j])
    return ingredientes


def load(ingredientes):
    # Lo pasamos a CSV
    pd.DataFrame(ingredientes).to_csv(
        'out/compra_semanal_2016.csv', header=True, index=None)


def create_report(pizza_types, orders, order_details, pizzas):
    csvs = [pizza_types, orders, order_details, pizzas]
    raiz = Element('Tipologia_Datos_Pizzeria_Maven')
    pizzas1 = SubElement(raiz, 'pizzas.csv', {'rows': '96'})
    orders1 = SubElement(raiz, 'orders.csv', {'rows': '21350'})
    order_details1 = SubElement(raiz, 'order_details.csv', {'rows': '48620'})
    pizza_types1 = SubElement(raiz, 'pizza_types.csv', {'rows': '32'})
    jerar_xml = [pizza_types1, orders1, order_details1, pizzas1]
    for i in range(len(csvs)):
        columnas = csvs[i].columns.values
        for j in columnas:
            col1 = SubElement(jerar_xml[i], str(j))
            tipo = str(csvs[i][j].dtype)
            a = csvs[i][j].isnull().value_counts()
            # si no ha encontrado ningun null que el numero total sea cero.
            n_nulls = a[1] if len(a) > 1 else 0
            atribs1 = SubElement(col1, 'atribs', {
                                 'type': f'{tipo}', 'nulls': f'{n_nulls}'})
    return raiz


def load_report(raiz):
    arbol = ET.ElementTree(raiz)
    arbol.write('out/reporte_tipologia.xml')


if __name__ == '__main__':
    pizza_types, orders, order_details, pizzas = extract()
    orders, order_details, pizza_types = transform(
        pizza_types, orders, order_details)
    ingredientes = get_ingredients_per_week(orders, order_details, pizza_types)
    raiz = create_report(pizza_types, orders, order_details, pizzas)
    load_report(raiz)
    load(ingredientes)
