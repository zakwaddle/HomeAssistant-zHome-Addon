const getUniqueLogValues = (array, key) => {
    return [...new Set(array.map(entry => entry['log'][key]))];
}

export default getUniqueLogValues;
