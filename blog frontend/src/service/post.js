import axios from 'axios';
import {observable} from 'mobx';
import store from 'store';
//import { pagination } from 'antd';

class PostService {

    constructor() {
        this.axios = axios.create({
            baseURL:'/api/post/'
        });
    }

    @observable msg='';
    @observable posts=[];
    @observable pagination={page:1, size:20, count:0, pages:0};
    @observable detail={};

    getJwt() {
        //验证token是否过期 
        //if (store.getExpiration('token')) return('over')
        return store.get('token', 'over');
    }

    //下面的axios如果没有this，就不能使用上面构造的基url，还是要用完整url
    pub(title, content) {
        console.log(title);
        this.axios.post('pub', {
            'title':title, 
            'content':content
        },{
            headers:{'jwt':this.getJwt()}
        }).then(
            response => {
                console.log(response.data, response.status);
                this.msg = '博文提交成功';
            }
        ).catch(
            error => {
                console.log(error);
                this.msg = '博文提交失败';
            }
        )
    }
    list(search) {
        // /list?page=1&size=2 -> constructor server list ?page=1&size=2-> 
        // list(?page=1&size=2) -> api/post/?page=1&size=2
        this.axios.get(search).then(
            response => {
                console.log(1,response),
                console.log(2,response.data)
                this.posts = response.data.posts;
                this.pagination = response.data.pagination;
            }
        ).catch(
            error => {
                console.log(error);
                this.msg = '文章列表加载失败';
            }
        )
    }

    getDetail(id) {
        this.axios.get(id).then(
            response => {this.detail = response.data.post}
        ).catch(
            error => {
                console.log(error),
                this.detail = {},
                this.msg = '文章加载失败';
            }
        )
    }
}

const postService = new PostService();
export {postService};





