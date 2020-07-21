# -*- coding: UTF-8 -*-

import sys
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
import aiomysql

from tornado.httpserver import HTTPServer
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio

from pythinkutils.common.log import g_logger
from pythinkutils.aio.auth.tornado.handler.BaseSimpleAuthHandler import *
from pythinkutils.common.StringUtils import *

g_szLoginPage = '''
<html>

<head>
    <meta charset="UTF-8">
    <title>Login</title>
    
    <style>
        body {
				    margin: 0;
				    padding: 0;
				    font-family: 'Raleway', sans-serif;
				    color: #F2F2F2;
				}
				
				#container-login {
				    background-color: #FCFCFC;
				    position: relative;
				    top: 20%;
				    margin: auto;
				    width: 340px;
				    height: 360px;
				    border-radius: 0.35em;
				    box-shadow: 0 3px 10px 0 rgba(0, 0, 0, 0.25);
				    text-align: center;
				}
				
				#container-register {
				    background-color: #FCFCFC;
				    position: relative;
				    top: 20%;
				    margin: auto;
				    width: 340px;
				    height: 480px;
				    border-radius: 0.35em;
				    box-shadow: 0 3px 10px 0 rgba(0, 0, 0, 0.25);
				    text-align: center;
				}
				
				#title {
				    position: relative;
				    background-color: #357ab5;
				    width: 100%;
				    padding: 20px 0px;
				    border-top-left-radius: 0.22em;
				    border-top-right-radius: 0.22em;
				    font-size: 22px;
				    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
				}
				
				.lock {
					position: relative;
					top: 2px;
				}
				
				.input {
					margin: auto;
				    width: 240px;
				    border-radius: 4px;
				    background-color: #ededed;
				    padding: 8px 0px;
				    margin-top: 15px;
				}
				
				.input-addon {
					position: relative;
					top: -2px;
				    float: left;
				    background-color: #ededed;
				    border: 1px solid #ededed;
				    padding: 4px 8px;
					color: #757575;
				    border-right: 1px solid #757575;
				}
				
				input[type=checkbox] {
					cursor: pointer;
				}
				
				input[type=text] {
					color: #949494;
				    margin: 0;
				    background-color: #ededed;
				    border: 1px solid #ededed;
				    padding: 6px 0px;
				    border-radius: 3px;
				}
				
				input[type=text]:focus {
				    border: 1px solid #ededed;
				}
				
				input[type=password] {
					color: #949494;
				    margin: 0;
				    background-color: #ededed;
				    border: 1px solid #ededed;
				    padding: 6px 0px;
				    border-radius: 3px;
				}
				
				input[type=password]:focus {
				    border: 1px solid #ededed;
				}
				
				input[type=email] {
					color: #949494;
				    margin: 0;
				    background-color: #ededed;
				    border: 1px solid #ededed;
				    padding: 6px 0px;
				    border-radius: 3px;
				}
				
				form {
						padding-top:36px
				}
				
				input[type=email]:focus {
				    border: 1px solid #ededed;
				}
				
				.forgot-password {
				    position: relative;
				    bottom: 0%;
				}
				
				.forgot-password a:link {
				    color: #f7c899;
				    text-decoration: none;
				}
				
				.forgot-password a:visited {
				    color: #f7c899;
				    text-decoration: none;
				}
				
				.forgot-password a:hover {
				    color: #449494;
				    transition: color 1s;
				}
				
				.privacy {
				    margin-top: 5px;
				    position: relative;
				    font-size: 12px;
				    bottom: 0%;
				}
				
				.privacy a:link {
				    color: #eaa05b;
				    text-decoration: none;
				}
				
				.privacy a:visited {
				    color: #eaa05b;
				    text-decoration: none;
				}
				
				.privacy a:hover {
				    color: #549494;
				    transition: color 1s;
				}
				
				*:focus {
				    outline: none;
				}
				
				.remember-me {
				    margin: 10px 0;
				}
				
				input[type=submit] {
				    padding: 12px 64px;
				    background: #629ce5;
				    color: #fff;
				    font-weight: bold;
				    border: 0 none;
				    cursor: pointer;
				    border-radius: 3px;
				    font-size: 16px;
				}
				
				.register {
					margin: auto;
				    padding: 16px 0;
				    text-align: center;
				    margin-top: 40px;
				    width: 85%;
				    border-top: 1px solid #C1C3C6;
				}
				
				.clearfix {
					clear: both;
				}
				
				#register-link {
				    margin-top: 10px;
				    padding: 6px 25px;
				    background: #FF7F4F;
				    color: #fff;
				    font-weight: bold;
				    border: 0 none;
				    cursor: pointer;
				    border-radius: 3px;
				}
				@font-face {
				  font-family: 'Raleway';
				  font-style: normal;
				  font-weight: 400;
				  unicode-range: U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF;
				}
				@font-face {
				  font-family: 'Raleway';
				  font-style: normal;
				  font-weight: 400;
				  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
				}
    </style>
</head>

<body>
    <div id="container-login">
        <div id="title">
            <i></i> Login
        </div>

        <form action="/login" method="POST">
            <div class="input">
            		<div class="input-addon">
                    <img height="24px" width="24px" src="data:image/png;base64,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" />
                </div>
                <input id="username" name="username" placeholder="Username" type="text" required class="validate" autocomplete="off">
            </div>

            <div class="clearfix"></div>

            <div class="input">
            		<div class="input-addon">
                    <img height="24px" width="24px" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEgAAABICAQAAAD/5HvMAAABo0lEQVR4Ae3Wz0qUURzH4UcHGmdbthddihL+2RZU5LY2kt1AKN2KKAZSuJS8ilpZiiGJVJbbsJXYNsegX9sazpAz75yJ4DyfG/jy/t7FUVRSFEVRFEVRjFmy5cCZCz98c2jLE6P0X82CHSHdrkdq+mjOsfhLR+7pi4YNccmeG5LZdfuig/YM553zWXTYx3yTGvZFF+2qy2JDdNlTGcyJrvvplh6rORYVOjSgpxZExR7oqR1RsVd6aEy07btlU+rqpq04F5n6w5KQ7otxv5tw0o9BW22/zrhWk5r5Bx2IZMtSVvMPOhPJpqTM5B90IZLVpTT+m0H5TzYtZfbf/dQrUtbyD3ohkp2b0OqGZv5BiyKdE5Mtc76K/INGRdvOrZrR0DBrTVNkqsVrUbGX2ot02vNQVOx+bwcN+iQqdGCgt4O4W+kJe5NeD+KZ6LI1cgwa8lZ00RtX8gxi2JHosPeukmsQw/ZEB+26Rs5BDFkXl2xdndyD4PYlTvfBHejPIAbN2xbpbJtXI/OghBGPbdp3qunCqXc2LRqRlH9QURRFURRFUfwCH+5+U3tYE1YAAAAASUVORK5CYII=" />
                </div>
                <input id="password" name="password" placeholder="Password" type="password" required class="validate" autocomplete="off">
            </div>

            <div class="remember-me">
                <input type="checkbox">
                <span style="color: #757575">Remember Me</span>
            </div>

            <input type="submit" value="Log In" />
            <input type="hidden" name="redirect_url" value="{redirect_url}" />
        </form>
				                    
				<!--
        <div class="forgot-password">
            <a href="#">Forgot your password?</a>
        </div>
        <div class="privacy">
            <a href="#">Privacy Policy</a>
        </div>

        <div class="register">
            <span style="color: #657575">Don't have an account yet?</span>
            <a href="#"><button id="register-link">Register here</button></a>
        </div>       
        -->
    </div>
</body>

</html>
'''

class ThinkLoginHandler(BaseSimpleAuthHandler):

    async def post(self):
        szUsername = self.get_argument("username", "")
        szPwd = self.get_argument("password", "")
        szRedirectUrl = self.get_argument("redirect_url", "")

        if is_empty_string(szUsername) or is_empty_string(szPwd):
            self.write(g_szLoginPage.replace("{redirect_url}", "/"))
        else:
            nUID, _szUsername, szToken = await self.login(szUsername, szPwd)
            if False == is_empty_string(szToken):
                if is_empty_string(szRedirectUrl):
                    self.redirect("/")
                else:
                    self.redirect(szRedirectUrl)
            else:
                self.redirect("/login")

    async def get(self):
        await self.post()