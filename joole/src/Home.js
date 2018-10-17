import React, { Component } from 'react';
import { withRouter } from "react-router-dom";
import { FomError } from "./"



const Button = ({history, target}) => {
    if(target){
        return (<button onClick = {() => {history.push(`/client/${target}`)}}>
                Go !
                </button>)
    } else {
        return <button>Desactivated</button>
    }
}

const RedirectButton = withRouter(Button)

class Home extends Component {
    constructor(props){
        super(props);
    
        this.state = {
            target: "",
            formError: false
        };

        this.handleChange = e =>{
            console.log(e.target.value)
            if (isNaN(e.target.value)){
                this.setState({
                    formError: true
                })
            } else {
                this.setState({
                    target: e.target.value,
                    formError: false
                })
            }
        }
    }


    render() {
        return (
        <div>
            <p>Home</p>
            <form>
                 Your client iD: <input 
                    onChange = {e =>this.handleChange(e) }
                    value = {this.state.target}
                 /> 
            </form>
            <FomError error={this.state.formError} />
            <RedirectButton target={this.state.target} />

        </div>
        )
    }
}

export default Home