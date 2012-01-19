# -*- coding: utf-8 -*-


def tagfy(tags, extension='html'):
    links = [A(" %s " % tag.strip(), _href=CURL('article', 'list', vars=dict(tag=tag), extension=extension)) for tag in tags]
    return CAT(*links)


DATEFORMAT = T("%Y-%m-%d")
TIMEFORMAT = T("%H:%M:%S")
current.TIMEFORMAT = TIMEFORMAT
current.DATEFORMAT = DATEFORMAT


def ftime(value):
    return value.strftime(str(DATEFORMAT))


from gluon.tools import prettydate
from datetime import datetime


def pdate(value):
    if isinstance(value, str):
        value = datetime.strptime(value, "%s %s" % (DATEFORMAT, TIMEFORMAT))
    return prettydate(value, T=T)

current.pdate = pdate
current.ftime = ftime


def ICONBUTTON(icon, text, action):
    bt = BUTTON(_class="ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-primary",
                _role="button",
                _onclick=action)
    bt.append(SPAN(_class="ui-button-icon-primary ui-icon ui-icon-%s" % icon))
    bt.append(SPAN(text, _class="ui-button-text"))

    return bt


def ICONLINK(icon, text, action=None):
    bt = A(_class="icon-link",
              _onclick=action,
              _style="cursor:pointer;")
    bt.append(CAT(
        IMG(_src=URL('static', 'basic/images/icons', args="%s.png" % icon), _width=16),
        SPAN(text, _style="line-height:16px;")
    ))

    return bt


def get_image(image, placeholder="image", themename='basic', user=None):
    if user:
        if user.photo_source == 1:
            if user.thumbnail:
                return URL('default', 'download', args=user.thumbnail, extension=False)
            # pass and let go to return default placeholder
        elif user.photo_source == 6:
            return user.googlepicture
        elif user.photo_source == 5:
            pass  # pass and let go to return default placeholder
        else:
            # try to get the image from the source
            from helpers.images import GetImages
            return GetImages.getphoto(user=user)

    if image and image.startswith("http://"):
        return image
    if image:
        return URL('default', 'download', args=image, extension=False)
    else:
        return URL('static', '%s/images' % themename, args='%s.png' % placeholder, extension=False)

current.get_image = get_image


def has_permission_to_edit(record):
    userid = session.auth.user.id if session.auth else 0
    return record.author == userid


c = 1


def getclass(columns=2):
    global c
    if c % columns == 0:
        c += 1
        return 'omega'
    else:
        c += 1
        return 'alpha'


current.getclass = getclass


def get_name_of(user):
    return "%(first_name)s %(last_name)s (%(nickname)s)" % user

search_form = FORM(
    DIV(
        SELECT(*[OPTION(option, _value=value) for value, option in [("article", T("Articles")), ("user", T("Users"))]], _name="kind", _id="kind"),
       _class="two columns alpha search-select"),
    DIV(
        INPUT(_type="search", _placeholder=T("Type word or name to find"), _name="q", _id="q"),
        BUTTON(IMG(_src=URL('static', 'images', args='search_button.png'))),
        _class="four columns omega search-input"
    ),
    _class="search-form",
    _method="GET",
    _action=CURL("home", "search")
)


response.menu = []

if session.auth:
    response.menu.append(
        (T('Create'), False, False, [
                                  (T('Content'), False, False, [
                                          (T('Article'), False, CURL('article', 'new', args='Article'), []),
                                          (T('Cook Recipe'), False, CURL('article', 'new', args='CookRecipe'), []),
                                          (T('Product'), False, CURL('article', 'new', args='Product'), []),
                                  ]),
                                  (T('Group'), False, False, [
                                
                                  ]),
                                  (T('Page'), False, False, [
                                          
                                  ])
                                  ]
                            )
                        )

    # CURL = ''

    response.menu.append(
         (T('Explore'), False, False, [
                                          (T('Find articles'), False, CURL('article', 'search'), []),
                                          (T('All articles'), False, CURL('article', 'list'), []),
                                          (T('Find members'), False, CURL('person', 'search'), []),
                                          (T('All members'), False, CURL('person', 'search', vars=dict(q='@')), []),
                                  ])
    )
    response.menu.append(
         (T('Me'), False, False, [
                                          (T('My profile'), False, CURL('person', 'show'), []),
                                          (T('My Settings'), False, CURL('person', 'account', args='profile'), []),
                                          (T('My content'), False, False,[
                                                 (T('My articles'), False, CURL('article', 'list', vars={'author': session.auth.user.id, 'limitby': '0,50'}), []),
                                                 (T('My drafts'), False, CURL('article', 'list', vars={'author': session.auth.user.id, 'limitby': '0,50'}), []),
                                                 (T('My pictures'), False, CURL('article', 'list', vars={'author': session.auth.user.id, 'limitby': '0,50'}), []),
                                                 (T('My favorited'), False, CURL('article', 'list', vars={'author': session.auth.user.id, 'limitby': '0,50'}), []),
                                                 (T('My liked'), False, CURL('article', 'list', vars={'author': session.auth.user.id, 'limitby': '0,50'}), []),
                                                 (T('My disliked'), False, CURL('article', 'list', vars={'author': session.auth.user.id, 'limitby': '0,50'}), []),
                                                 (T('My subscriptions'), False, CURL('article', 'list', vars={'author': session.auth.user.id, 'limitby': '0,50'}), []),
                                                 (T('My comments'), False, CURL('article', 'list', vars={'author': session.auth.user.id, 'limitby': '0,50'}), []),
                                                 (T('My Recipe Book'), False, CURL('article', 'list', vars={'author': session.auth.user.id, 'limitby': '0,50'}), []),
                                          ]),
                                          (T('My contacts'), False, CURL('person', 'contacts'), []),
                                          (T('My pages'), False, False, []),
                                          (T('My groups'), False, False, []),
                                          (T('My Activities'), False, CURL('person', 'usertimeline'), []),
                                          (T('My Board'), False, CURL('person', 'usertimeline'), []),
                                          (T('My Messages'), False, False, []),
                                          (T('Logout'), False, CURL('default', 'user', args='logout'), []),
                                  ])
    )
    response.menu.append((DIV(IMG(_src=URL('static', 'images', args='alert.18.png'), alt=T("Alert"), title=T("Notifications")), " (1)", _onclick="alert('Sorry, notifications page is under construction!')"), False, False, []))
else:
    response.menu.append((T('Login'), False, CURL('person', 'account', args='login'), []))
    response.menu.append((T('Join'), False, CURL('person', 'account', args='register'), []))

response.menu.append((T('GitHub'), False, "http://github.com/rochacbruno/Movuca", []))

# events

event_info = dict(new_article={'url_to': CURL('article', 'show', extension=False),
                                 'url': CURL('person', 'show', extension=False),
                                 'icon': "attach_round.24.png",
                                 'title': T(" added a new %(event_to)s"),
                                 'smalltitle': T("added a new content"),
                                 },
                    update_article={'url_to': CURL('article', 'show', extension=False),
                                     'url': CURL('person', 'show', extension=False),
                                     'icon': "pen_rounded.24.png",
                                    'title': T(" updated an %(event_to)s"),
                                    'smalltitle': T("updated"),
                                    },
                    new_contact={'url_to': CURL('person', 'show', extension=False),
                                 'url': CURL('person', 'show', extension=False),
                                 'icon': "edge_arrow_right.24.png",
                                 'title': T(" followed %(event_to)s"),
                                 'smalltitle': T("followed"),
                                 },
                    new_article_comment={'url_to': CURL('article', 'show', extension=False),
                                         'url': CURL('person', 'show', extension=False),
                                         'icon': "black_board.24.png",
                                         'title': T(" commented on %(event_to)s")},
                    liked={'url_to': CURL('article', 'show', extension=False),
                           'url': CURL('person', 'show', extension=False),
                           'icon': "like_rounded.24.png",
                           'title': T(" liked the %(event_to)s")},
                    subscribed={'url_to': CURL('article', 'show', extension=False),
                                'url': CURL('person', 'show', extension=False),
                                 'icon': "subscribe.png",
                                'title': T(" subscribed to %(event_to)s updates")},
                    favorited={'url_to': CURL('article', 'show', extension=False),
                               'url': CURL('person', 'show', extension=False),
                               'icon': "favorite.png",
                               'title': T(" favorited the %(event_to)s")},
                    disliked={'url_to': CURL('article', 'show', extension=False),
                              'url': CURL('person', 'show', extension=False),
                              'icon': "dislike.png",
                              'title': T(" disliked the %(event_to)s")},
                    new_picture={'url': CURL(),
                                 'url_to': CURL('article', 'show', extension=False),
                                 'title': ""},
                    new_picture_comment={'url': CURL(),
                                         'url_to': CURL('article', 'show', extension=False),
                                         'title': ""},
                    wrote_on_wall={'url': CURL('person', 'show', extension=False),
                                   'url_to': CURL('person', 'show', extension=False),
                                   'icon': "board.24.png",
                                   'title': T(" wrote on %(event_to)s board")})
