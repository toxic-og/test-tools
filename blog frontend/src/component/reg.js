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
export default class Reg extends React.Component {
    validatePwd(pwd1, pwd2) {
        return pwd1.value === pwd2.value 
    }

    handleClick(event) {
        event.preventDefault();
        console.log(event);
        const [name, email, passwd, confirm, phnumber] = event.target.form;
        console.log(this.validatePwd(passwd, confirm, phnumber));
        this.props.service.reg(name.value, email.value, passwd.value, phnumber.value);
    }
    render() {
        if(this.props.service.loggedin) {
            return <Redirect to='/' />;
        }

        let em = this.props.service.errMsg;

        return (
            <div className='login-page'>
                <div className='form'>
                    <form className='register-form'>
                        <input type='text' placeholder='用户名' />
                        <input type='text' placeholder='邮箱' />
                        <input type='password' placeholder='密码' />
                        <input type='password' placeholder='确认密码' />
                        <input type='text' placeholder='手机号' /> 
                        <button onClick={this.handleClick.bind(this)}>注册</button>
                        <p className='massage'>如果已经注册<Link to='/login'>请登录</Link></p>
                    </form>
                </div>
            </div>
        )
    };
    
    componentDidUpdate(prevProps,prevState) {
        if (prevProps.service.errMsg) {
            message.info(prevProps.service.errMsg, 3, () => prevProps.service.errMsg='');
        }
    }
};

