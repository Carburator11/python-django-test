import React from 'react';

const FormError = ({error=false})=>{
    if(error){
        return <p style={{'color': 'red'}}>Please provide only numbers</p>
    } else {
        return null
    }
}

export default FormError