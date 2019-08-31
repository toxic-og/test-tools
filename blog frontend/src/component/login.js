import React from 'react';
import {Link, Redirect} from 'react-router-dom';
import '../css/login.css';
import {userService as service} from '../service/user';
import {observer} from 'mobx-react';
import {message} from 'antd';
import 'antd/lib/message/style';
import {inject} from '../utils';

@inject({service})
@observer
export default class Login extends React.Component {
    handleClick(event) {
        event.preventDefault();
        const fm = event.target.form;
        console.log(fm);
        this.props.service.login(
            fm[0].value, fm[1].value
        );
     }
    render() {
        if (this.props.service.loggedin) {
            return <Redirect to='/' />;
        }

        let em = this.props.service.errMsg;

        return (
            <div className='login-page'>
                <div className='form'>
                    <form className='login-form'>
                        <input type='text' placeholder='邮箱' />
                        <input type='password' placeholder='密码' />
                        <button onClick={this.handleClick.bind(this)}>登录</button>
                        <p className='massage'>还未注册？<Link to='/reg'>请注册</Link> </p>
                    </form>
                </div>
            </div>
        )
    }
    
    componentDidUpdate(prevProps,prevState) {
        if (prevProps.service.errMsg) {
            message.info(prevProps.service.errMsg, 3, () => prevProps.service.errMsg='');
        }
    }
}







