context = {
    "last_intent": None,
    "mode": None,
    "troubleshoot_step": 0,
    "troubleshoot_type": None,
    "troubleshoot_data": {},
    "waiting_for_follow_up": False 
}

def update_context(intent, user_input=None):
    global context
    context["last_intent"] = intent
    if user_input:
        context["last_user_input"] = user_input

def reset_context():
    global context
    context = {
        "last_intent": None,
        "mode": None,
        "troubleshoot_step": 0,
        "troubleshoot_type": None,
        "troubleshoot_data": {}
    }

def set_mode(mode):
    global context
    context["mode"] = mode

def get_mode():
    return context.get("mode")