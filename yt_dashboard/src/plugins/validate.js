
function required(message='Is required'){
    return (value) => (!!value || value === 0) || message;
}
function isDate(reverseDate, message='Geen date'){

    function reverse(date){
      const [day, month, year] = date.split('-')
      return `${year}-${month}-${day}`
    }

    return (v) => {

        let d = new Date(v)

        if(reverseDate && v){
            d = new Date(reverse(v))
        }

        if(d instanceof Date && !isNaN(d)){
            return true
        }else{
            return message
        }
    }
}

function isNumeric(message = 'Is niet numeriek') {
    return (v) => /^-?\d+$/.test(v) || message;
}
// also found this
// function IsNumeric(input)
// {
//     return (input - 0) == input && (''+input).trim().length > 0;
// }

//does this has floats?:
// export function isNumeric(value: any): boolean {
//     return !isNaN(value - parseFloat(value));
// }

//deze is ook populair (angular):
function isFloat(message = 'Is geen decimaal getal') {
    return (v) => (!isNaN(parseFloat(v)) && isFinite(v)) || message
}

function isNumericAndPositive(message = 'Is niet numeriek en positief') {
    return (v) => /^\d+$/.test(v) || message
}

function max(maxValue,message='Dit getal is te groot') {
    return (v) => {

        if(v <= maxValue){
            return true
        }else{
            return message
        }
    }
}
function min(minValue,message='Dit getal is te klein') {
    return (v) => {

        if(v > minValue){
            return true
        }else{
            return message
        }
    }
}

function alphaNumeric(message='Het veld mag alleen a-z, 0-9 of een spatie bevatten'){
    return (v) => /^[0-9a-zA-Z ]+$/.test(v) || message
}

function namesAndSpecials(message='Deze tekens zijn niet correct'){
    return (v) => {
        return /^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$/.test(v) || message
    }

}

export { required, isDate, isNumeric, isNumericAndPositive, isFloat, max, min, alphaNumeric, namesAndSpecials }

