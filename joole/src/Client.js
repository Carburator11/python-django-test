import React, { Component } from 'react';
import { ClientDashboard, Loader } from "./"
import {params} from './config'

const fetchData = (id, cb) => {
    const API = "/api/client"
    const url = `${API}/${id}`
    console.log(url)
    fetch(url, params.get)
        .then(response => {
            console.log("Response ", response)
            response.json()
        .then(data => {
            console.log("Data", data)
            return cb(data)
            });
        })
}

class Client extends Component {

    constructor(props) {
        super(props);
    
        this.state = {
            clientData: {},
            id: this.props.match.params.id
        };
    }
    
    componentDidMount() {
        fetchData(this.state.id, data => this.setState({clientData: data}))
    }
    
    
    render() {
        const data = this.state.clientData
        if(true){
        // if (data && data.length > 0){
            return (
                <div>
                    <p>Client id: {this.state.id}</p>
                    <ClientDashboard data = {data} />
                </div>
            )
        } else {
            return <Loader />
        }
    }
}

export default Client