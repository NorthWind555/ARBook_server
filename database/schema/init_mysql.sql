DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`
(
    `id`          int(11)  auto_increment COMMENT '主键',
    `name`        varchar(24) COMMENT '姓名',
    `phone`       varchar(11) COMMENT '手机号',
    `nickname`    varchar(64) COMMENT '用户名',
    `password`    varchar(64) NOT NULL COMMENT '密码',
    `avatar`      varchar(512) COMMENT '头像',
    `school`      varchar(64) COMMENT '学校',
    `college`     varchar(64) COMMENT '学院',
    `clazz`       varchar(64) COMMENT '班级',
    `sex`         tinyint DEFAULT 0 COMMENT '0未知 1男 2女',
    `status`      tinyint  DEFAULT 0 COMMENT '状态 0:正常，1:禁用',
    `client_host` varchar(19) COMMENT '访问IP',
    `create_time` datetime COMMENT '创建时间',
    `update_time` datetime COMMENT '更新时间',
    `del_flag`    tinyint  DEFAULT 0 COMMENT '删除标记 0正常',
    PRIMARY KEY (`id`)
);