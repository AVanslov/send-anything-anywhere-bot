id='8543530040286985983' 
from_user=User(
    id=6284162894, 
    is_bot=False, 
    first_name='Aleksandr', 
    last_name='Buchelnikov', 
    username='aleksandr_buchelnikov', 
    language_code='en', 
    is_premium=None, 
    added_to_attachment_menu=None, 
    can_join_groups=None, 
    can_read_all_group_messages=None, 
    supports_inline_queries=None, 
    can_connect_to_business=None
) 
chat_instance='-2138748713627800148' 
message=Message(
    message_id=156, 
    date=datetime.datetime(2024, 6, 8, 8, 31, 4, tzinfo=TzInfo(UTC)), 
    chat=Chat(
        id=6284162894, 
        type='private', 
        title=None, 
        username='aleksandr_buchelnikov', 
        first_name='Aleksandr', 
        last_name='Buchelnikov', 
        is_forum=None, 
        accent_color_id=None, 
        active_usernames=None, 
        available_reactions=None, 
        background_custom_emoji_id=None, 
        bio=None, 
        birthdate=None, 
        business_intro=None, 
        business_location=None, 
        business_opening_hours=None, 
        can_set_sticker_set=None, 
        custom_emoji_sticker_set_name=None, 
        description=None, 
        emoji_status_custom_emoji_id=None, 
        emoji_status_expiration_date=None, 
        has_aggressive_anti_spam_enabled=None, 
        has_hidden_members=None, 
        has_private_forwards=None, 
        has_protected_content=None, 
        has_restricted_voice_and_video_messages=None, 
        has_visible_history=None, 
        invite_link=None, 
        join_by_request=None, 
        join_to_send_messages=None, 
        linked_chat_id=None, 
        location=None, 
        message_auto_delete_time=None, 
        permissions=None, 
        personal_chat=None, 
        photo=None, 
        pinned_message=None, 
        profile_accent_color_id=None, 
        profile_background_custom_emoji_id=None, 
        slow_mode_delay=None, 
        sticker_set_name=None, 
        unrestrict_boost_count=None
    ), 
    message_thread_id=None, 
    from_user=User(
        id=6475550637, 
        is_bot=True, 
        first_name='SendAnythingAnywhereBot', 
        last_name=None, 
        username='SendAnythingAnywhereBot', 
        language_code=None, 
        is_premium=None, 
        added_to_attachment_menu=None, 
        can_join_groups=None, 
        can_read_all_group_messages=None, 
        supports_inline_queries=None, 
        can_connect_to_business=None
    ), 
    sender_chat=None, 
    sender_boost_count=None, 
    sender_business_bot=None, 
    business_connection_id=None, 
    forward_origin=None, 
    is_topic_message=None, 
    is_automatic_forward=None, 
    reply_to_message=None, 
    external_reply=None, 
    quote=None, reply_to_story=None, via_bot=None, edit_date=None, has_protected_content=None, is_from_offline=None, media_group_id=None, 
    author_signature=None, text='Введите желаемую дату доставки в формате дд/мм/гггг, например, 01/01/2024', entities=None, link_preview_options=None, 
    effect_id=None, animation=None, audio=None, document=None, photo=None, sticker=None, story=None, video=None, video_note=None, voice=None, 
    caption=None, caption_entities=None, show_caption_above_media=None, has_media_spoiler=None, contact=None, dice=None, game=None, poll=None, 
    venue=None, location=None, new_chat_members=None, left_chat_member=None, new_chat_title=None, new_chat_photo=None, delete_chat_photo=None, 
    group_chat_created=None, supergroup_chat_created=None, channel_chat_created=None, message_auto_delete_timer_changed=None, migrate_to_chat_id=None, 
    migrate_from_chat_id=None, pinned_message=None, invoice=None, successful_payment=None, users_shared=None, chat_shared=None, connected_website=None, 
    write_access_allowed=None, passport_data=None, proximity_alert_triggered=None, boost_added=None, chat_background_set=None, forum_topic_created=None, 
    forum_topic_edited=None, forum_topic_closed=None, forum_topic_reopened=None, general_forum_topic_hidden=None, general_forum_topic_unhidden=None, 
    giveaway_created=None, giveaway=None, giveaway_winners=None, giveaway_completed=None, video_chat_scheduled=None, video_chat_started=None, 
    video_chat_ended=None, video_chat_participants_invited=None, web_app_data=None, 
    reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='Хочу отправить', url=None, callback_data='want_to_send', web_app=None, login_url=None, 
                switch_inline_query=None, switch_inline_query_current_chat=None, switch_inline_query_chosen_chat=None, callback_game=None, pay=None)], 
            [InlineKeyboardButton(
                text='Хочу доставить', url=None, callback_data='want_to_delivery', 
                web_app=None, login_url=None, switch_inline_query=None, switch_inline_query_current_chat=None, switch_inline_query_chosen_chat=None, 
                callback_game=None, pay=None)], 
            [InlineKeyboardButton(
                text='Избранное', url=None, callback_data='Favorite', web_app=None, login_url=None, switch_inline_query=None, 
                switch_inline_query_current_chat=None, switch_inline_query_chosen_chat=None, callback_game=None, pay=None)], 
            [InlineKeyboardButton(
                text='Посмотреть историю посылок', url=None, callback_data='see_orders_history', web_app=None, login_url=None, 
                switch_inline_query=None, switch_inline_query_current_chat=None, switch_inline_query_chosen_chat=None, callback_game=None, pay=None)], 
            [InlineKeyboardButton(
                text='Посмотреть доступные направления', url=None, callback_data='see_availible_routes', web_app=None, login_url=None, 
                switch_inline_query=None, switch_inline_query_current_chat=None, switch_inline_query_chosen_chat=None, callback_game=None, pay=None)], 
            [InlineKeyboardButton(
                text='Сделать донат', url=None, callback_data='send_money', web_app=None, login_url=None, switch_inline_query=None, 
                switch_inline_query_current_chat=None, switch_inline_query_chosen_chat=None, callback_game=None, pay=None)], 
            [InlineKeyboardButton(
                text='Написать разработчику', url=None, callback_data='contact_developer', web_app=None, login_url=None, switch_inline_query=None, 
                switch_inline_query_current_chat=None, switch_inline_query_chosen_chat=None, callback_game=None, pay=None)
            ]
        ]
    ), 
    forward_date=None, forward_from=None, forward_from_chat=None, forward_from_message_id=None, forward_sender_name=None, 
    forward_signature=None, user_shared=None
) 
inline_message_id=None 
data='want_to_delivery' 
game_short_name=None