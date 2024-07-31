def bodyMass():
    weight = float(input('Cual es tu peso en kilos? '))
    height = float(input('Cual es tu estatura en metros? '))
    assert weight > 0 and height > 0
    return f'Tu bmi es de: {weight / height}'

print(bodyMass())
