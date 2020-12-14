#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/9/18 15:20
# @Site    :
# @File    : response_code_msg.py
# @Software: PyCharm
"""


class ResponseCode(object):
    Success = 200  # 成功
    DeleteSuccess = 202
    Fail = 500  # 失败
    NoResourceFound = 404  # 未找到资源
    InvalidParameter = 400  # 参数无效
    Forbidden = 403  # 被拒绝
    ExpectationFailed = 417
    AuthFailed = 401


class ResponseMessage(object):
    CommentSuccess = "更改管理员提问状态成功"
    SuccessEditUser = "更改用户信息成功"
    SuccessDeleteRoom = "删除房间成功"
    SuccessAddRoom = "新增房间成功"
    SuccesUnBind = "成功绑定"
    Success = "成功"
    Fail = "失败"
    DateErr = "日期格式有误"
    DateltErr = "选择的日期在当前日期之前"
    ResisterSuccess = "注册用户成功"
    isLoginErr = "请先登录"
    LoginTypeErr = "登录类型错误"
    NoResourceFound = "未找到资源"
    InvalidParameter = "参数无效"
    AccountOrPassWordErr = "账户或密码错误"
    LoginTypeForbidden = "当前用户无权限访问web服务端"
    NoUserErr = "当前用户不存在"
    IllegalStrErr = "用户名存在非法字符：只能是数字、字母、下划线组合"
    RepeatUserErr = "用户重复创建"
    FatherUserErr = "主用户不存在"
    PasswordNoMatchErr = "两次密码不一致"
    PasswordRequireErr = "新密码或旧密码为必填"
    ResetPasswordToPhoneErr = "重置密码为手机号成功"
    DeleteErr = "没有要删除数据"
    BadRquest = "错误的请求"
    TokeninvalidErr = "传入无效的token"
    TokenForbiddenErr = "Token过期了，请重新登录"
    TokenForbiddenAddErr = "Token过期了，请客户端刷新Token"
    IllegalPictureErr = "图片上传格式有误，(要求png或jpg)"
    JurisdictionErr = "权限不足，无法访问"
    LoginVerifyErr = "登录失败验证不通过"
    PictureExistErr = "图片已存在"
    ParseDataErr = "训练报告数据解析错误"
    VerificationCodeError = "验证码错误"
    PleaseSignIn = "请登陆"
    TokenFlush = "刷新Token"
    SuperLimit = "超级管理用户无法登陆"
    CommonLimit = "用户非法登陆"
    AdminLimit = "管理员用户无法登陆"
    CountLimit = "人数上限无法添加用户"

    InstitutionUserErr = "机构名称已经存在"
    InstitutionCodeErr = "机构码已经存在"
    InstitutionAccountErr = "机构注册账号重复"
    InstitutionLoginAccountErr = "机构账号不存在"

    ExcelUserErr = "上传EXCEL解析出错，请按模版填写"
    ExcelUserValidataErr = "上传数据EXCEL规则错误"
    DrawPngErr = "生成hrv训练图片失败"
    ExpireErr = "当前机构已到期，请联系超级管理员"
    TokenOnceErr = "当前验证失效,有效0次数"

    DeviceLoginAccountErr = "设备编号不存在"
    TimeFormatError = "时间序列化错误"

    FingerIsOpenErr = "指纹已经开通不能重复开通"

    DeviceTypeErr = "没有此设备类型"
    DeviceExistsErr = "当前设备码已存在"
    ResisterDeviceSuccess = "注册设备成功"
    DeviceErr = "请求设备非法"
    GameTypeNotExist = "游戏类型不存在"

    VrBindErr = "该用户已绑定，无法重复绑定"
    SuccessBindVr = "VR设备绑定成功"
    VrUnBindErr = "解绑VR设备失败"
    SuccessUnBindVr = "解绑VR设备成功"
    VRNoData = "目前没有训练数据"
    VRNoUserTrainErr = "当前没有VR用户训练"
    ServiceNotOnline = "服务端不在线，无法发送训练场景"
    SuccessWebControl = "发送控制场景指令成功"
    ShortHrvDataErr = "训练时间过短无法进行数据保存"
    NotBindErr = "当前训练数据未进行监控"

    isLoginWebEegErr = "请先登录脑电web端服务"
    ServiceLoginFirstErr = "请先登录服务端"
    ExistsIdCardUser = "当前身份证已经被注册"
    MaxBindUserErr = "超过最大绑定用户"
    RoomNoBindErr = "当前方面没有绑定用户"

    NotFoundDeviceCode = "设备码不存在"
    NotFoundUser = "用户不存在"
    NotFondDeviceStatistic = "未注册该统计信息"
    DateTimeParmesErr = "时间解析错误"
    AppTrainLimit = "apphrv训练，达到最大人数。"
