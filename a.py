def max_consecutive_variants(arr):
    max_consecutive = {}
    current_variant = arr[0]
    current_count = 1

    for char in arr[1:]:
        if char == current_variant:
            current_count += 1
        else:
            max_consecutive[current_variant] = max(max_consecutive.get(current_variant, 0), current_count)
            current_variant = char
            current_count = 1
    max_consecutive[current_variant] = max(max_consecutive.get(current_variant, 0), current_count)
    return max_consecutive

# Ejemplo de uso
arr = ['y', 'o', 'o', 'o', 'y', 'y', 'p', 'o', 'o']
print("Lista:", arr)
result = max_consecutive_variants(arr)
print("Máximas consecutivas:", result)


#function that counts the number of =3, =4 and =5 consecutive candies, use the result from the previous function
#example result: {'y': 2, 'o': 3, 'p': 1}
def count_consecutive_candies(dictionary):
    count_consecutives = {
        '3': 0,
        '4': 0,
        '5': 0
    }
    
    for key, value in dictionary.items():
        if value == 3:
            count_consecutives['3'] += 1
        elif value == 4:
            count_consecutives['4'] += 1
        elif value == 5:
            count_consecutives['5'] += 1

    return count_consecutives

# Ejemplo de uso
result = count_consecutive_candies(result)
print("Consecutivos:", result)



