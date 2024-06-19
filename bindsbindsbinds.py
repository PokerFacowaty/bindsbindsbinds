import keyboard
import mouse
import yaml
from collections import defaultdict
import time

keysets = {}
current_keyset = None
mouse_binds_in_current_keyset = {}


def main():
    # {keyset_name: {source_key: [destination_keys]}}
    global keysets
    keysets = parse_and_map_binds()
    bind_keysets(keysets, verbose=True)
    keyboard.wait()


def parse_and_map_binds():
    '''Parses keybinds from yaml and rebuilds the structure so that it's
    a dict of source keys as keys and multiple resulting keys as values, to
    allow for multibinding.'''

    with open(".\\binds.yaml", "r", encoding='utf-8') as f:
        # {name: {destination_key: source_keys}}
        keysets_destination2sources = yaml.safe_load(f)
    # {name: {source_key: destination_keys}
    names_source2destinations = {}
    for set_name, destination2sources in keysets_destination2sources.items():
        names_source2destinations[set_name] = defaultdict(list)
        for destination, sources in destination2sources.items():
            for source in sources.split(','):
                names_source2destinations[set_name][source].append(destination)
    return names_source2destinations


def bind_keysets(keysets, verbose=False):
    '''Binds keysets so Ctrl+Alt combinations'''
    for index, keyset_name in enumerate(keysets.keys()):
        if verbose:
            print(f"\nSetting Ctrl+Alt+{str(index + 1)} for the keybind set"
                  + f"'{keyset_name}'")

        keyboard.add_hotkey(f'ctrl+alt+{index + 1}', switch_to_keyset,
                            args=(keysets, f"{keyset_name}"))


def switch_to_keyset(keysets, keyset_name):
    '''Changes the current mapping to the chosen keyset'''
    # cleanup
    keyboard.release('ctrl+alt')
    global current_keyset
    if current_keyset is not None:
        for key in keysets[current_keyset].keys():
            if key not in ['lmb', 'rmb', 'mmb', 'wheelup', 'wheeldn']:
                # .unhook_all() doesn't release keys pressed somewhere in the
                # middle of the transition, this is an attempt at solving it
                keyboard.release(key)
    keyboard.unhook_all()
    mouse.unhook_all()

    current_keyset = keyset_name
    global current_keyset_mouse
    current_keyset_mouse = {}
    # Binding them to Ctrl+Alt combinations again since unhook_all() wiped it
    bind_keysets(keysets)
    keyset = keysets[keyset_name]
    global mouse_binds_in_current_keyset
    
    keyboard.add_hotkey('alt+tab', keyboard.send, args=['alt+tab'])

    mouse.hook(handle_mouse)

    # Let's just assume the text will never be longer than 79
    print(" " * 79, end="\r", flush=True)
    print(f"Current keyset: {current_keyset}", end="\r", flush=True)

    for source, destinations in keyset.items():
        if source in ['lmb', 'rmb', 'mmb', 'wheelup', 'wheeldn']:
            mouse_binds_in_current_keyset[source] = '+'.join(destinations)
            continue
        destination_keys = []
        for destination in destinations:
            # Ignoring mouse keys as destinations
            if destination not in ['lmb', 'rmb', 'mmb', 'wheelup', 'wheeldn']:
                destination_keys.append(destination)
        keyboard.remap_key(source, '+'.join(destination_keys))


def handle_mouse(e):
    # e will either be mouse.ButtonEvent, mouse.MoveEvent (ignored) or
    # mouse.WheelEvent
    global mouse_binds_in_current_keyset
    if isinstance(e, mouse.ButtonEvent):
        if e.event_type == mouse.DOWN or e.event_type == mouse.DOUBLE:
            proper_name = {'left': 'lmb', 'right': 'rmb',
                           'middle': 'mmb'}[e.button]
            destinations = mouse_binds_in_current_keyset[proper_name]
            keyboard.press(destinations)
        elif e.event_type == mouse.UP:
            proper_name = {'left': 'lmb', 'right': 'rmb',
                           'middle': 'mmb'}[e.button]
            destinations = mouse_binds_in_current_keyset[proper_name]
            keyboard.release(destinations)
    elif isinstance(e, mouse.WheelEvent):
        if e.delta > 0:
            # keys hardly ever register if you use keyboard.send()
            keyboard.press(mouse_binds_in_current_keyset['wheelup'])
            time.sleep(0.03)
            keyboard.release(mouse_binds_in_current_keyset['wheelup'])
        elif e.delta < 0:
            keyboard.press(mouse_binds_in_current_keyset['wheeldn'])
            time.sleep(0.03)
            keyboard.release(mouse_binds_in_current_keyset['wheeldn'])


if __name__ == "__main__":
    main()
