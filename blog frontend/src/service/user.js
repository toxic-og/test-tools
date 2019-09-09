import axios from 'axios'
import store from 'store'
import {observable} from 'mobx'

store.addPlugin(require('store/plugins/expire')) //加载过期插件
class UserService {
    @observable loggedin = false;
    @observable errMsg = '';
    login (email, passwd) {
        console.log(email, passwd);
        axios.post('/api/user/login',{
            email:email,
            password:passwd
        }).then(response => {
            // console.log(response);
            // console.log(response.config);
            // console.log(response.data);
            // console.log(response.status);
            const {token, user} = response.data;
            //设置过期时间
            store.set('token',token,(new Date()).getTime() + (8*3600*1000));
            this.loggedin = true;
        }).catch(error => {
            console.log(error),
            this.errMsg = '登录失败';
        })
    }

    reg(name, email, passwd) {
        console.log(name, email, passwd);
        axios.post('/api/user/reg', {
            'email':email,
            'passwd':passwd,
            'name':name
        }).then(
            response => {
                console.log(response.data, response.status);
                store.set('token', 
                response.data.token, 
                (new Date()).getTime()+(8*3600*1000));
                this.loggedin = true;
            }
        ).catch(
            error => {
                console.log(error),
                this.errMsg = '注册失败';
            }
        )
    }
};
const userService = new UserService();
export {userService};




