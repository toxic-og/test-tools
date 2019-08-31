import React from 'react';
import {inject} from '../utils';
import {postService as service} from '../service/post';
import {observer} from 'mobx-react';
import {List, pagination} from 'antd';
import {Link} from 'react-router-dom';

import 'antd/lib/List/style';
import 'antd/lib/pagination/style';

@inject({service})
@observer
export default class L extends React.Component {
    constructor(props) {
        super(props);
        props.service.list(props.location.search);
    }
    handleChange(page, pageSize) {
        let search = `?page=${page}&size=${pageSize}`;
        this.props.service.list(search);
    }
    
    render() {
        let data = this.props.service.posts;
        if(data.length){
            const {
                page:current=1, size:pageSize=20, count:total=0
                } = this.props.service.pagination;
            return(
                <List header={<div>博文列表</div>}
                footer={<div>数据内容</div>}
                bordered
                dataSource={data}
                renderItem={item => (
                <List.Item>
                    <Link to={'/post'+item.post_id}>{item.title}</Link>
                </List.Item>
                )}
                pagination={{
                    current:current,
                    total:total,
                    pageSize:pageSize,
                    onChange:this.handleChange.bind(this)
                }}
                />
            ) 
        }
        else
            return(
                <div>无数据</div>
            );
    }
}