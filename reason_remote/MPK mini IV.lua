-- Track SHIFT state for modifier functions
g_shift_held = false
g_is_playing = false

function remote_init()
    local items = {
        -- Keyboard
        { name="Keyboard", input="keyboard" },

        -- Transport
        { name="Play", input="button" },
        { name="Stop", input="button" },
        { name="Loop", input="button" },
        { name="Record", input="button" },
        { name="Quantize", input="button" },
        { name="Forward", input="button" },
        { name="Undo", input="button" },
        { name="Redo", input="button" },
        { name="Tap Tempo", input="button" },
        { name="Click", input="button" },

        -- Bank navigation
        { name="Bank -", input="button" },
        { name="Bank +", input="button" },

        -- Joystick
        { name="Pitch Bend", input="value", min=0, max=16383 },
        { name="Mod Wheel", input="value", min=0, max=127 },

        -- Knobs
        { name="Knob 1", input="value", min=0, max=127 },
        { name="Knob 2", input="value", min=0, max=127 },
        { name="Knob 3", input="value", min=0, max=127 },
        { name="Knob 4", input="value", min=0, max=127 },
        { name="Knob 5", input="value", min=0, max=127 },
        { name="Knob 6", input="value", min=0, max=127 },
        { name="Knob 7", input="value", min=0, max=127 },
        { name="Knob 8", input="value", min=0, max=127 },

        -- Pads are handled as Keyboard notes (channel 10)
        -- They pass through as MIDI notes to Kong/Redrum
    }
    remote.define_items(items)

    -- Build index lookup
    g_items = {}
    for i, item in ipairs(items) do
        g_items[item.name] = i
    end

    local inputs = {
        -- Transport buttons come from DAW Port (port=1)
        { pattern="b0 4a xx", name="Loop", port=1 },        -- CC 74
        { pattern="b0 4e xx", name="Forward", port=1 },     -- CC 78

        -- Bank navigation buttons come from DAW Port (port=1)
        { pattern="b0 0f xx", name="Bank -", port=1 },      -- CC 15
        { pattern="b0 10 xx", name="Bank +", port=1 },      -- CC 16

        -- Joystick comes from MIDI Port (port=2)
        { pattern="e? xx yy", name="Pitch Bend", value="y*128 + x", port=2 },
        { pattern="b? 01 xx", name="Mod Wheel", port=2 },

        -- Knobs (Channel 1, CC 24-31) come from MIDI Port (port=2)
        { pattern="b0 18 xx", name="Knob 1", port=2 },
        { pattern="b0 19 xx", name="Knob 2", port=2 },
        { pattern="b0 1a xx", name="Knob 3", port=2 },
        { pattern="b0 1b xx", name="Knob 4", port=2 },
        { pattern="b0 1c xx", name="Knob 5", port=2 },
        { pattern="b0 1d xx", name="Knob 6", port=2 },
        { pattern="b0 1e xx", name="Knob 7", port=2 },
        { pattern="b0 1f xx", name="Knob 8", port=2 },

        -- Keyboard handles ALL notes including channel 10 pads (from MIDI Port)
        -- Pads will play as notes on the target instrument (Kong, Redrum, etc.)
        {pattern="8? xx yy", name="Keyboard", value="0", note="x", velocity="64", port=2},
        {pattern="9? xx 00", name="Keyboard", value="0", note="x", velocity="64", port=2},
        {pattern="<100x>? yy zz", name="Keyboard", port=2},
    }
    remote.define_auto_inputs(inputs)
end

function remote_probe()
    local controlRequest = "F0 7E 7F 06 01 F7"
    local controlResponse = "F0 7E 7F 06 02 47 5D 00 19 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? F7"
    return {
        request = controlRequest,
        response = controlResponse
    }
end

function remote_prepare_for_use()
    -- Send Kong-compatible preset to MPK Mini IV preset slot 2
    -- This remaps pads to C1-D#2 (notes 36-51) for Kong/Redrum compatibility
    -- Pads 1-16 on controller map directly to Kong/Redrum pads 1-16
    -- NOTE: User must select preset 2 on controller (PROG SELECT + Pad 2)
    -- NOTE: Arpeggiator clock source cannot be set via SysEx (firmware limitation)
    --       User must manually set External clock: SHIFT + ARP → Clock → EXT
    return {
        remote.make_midi("F0 47 00 5D 67 02 3B 02 52 65 61 73 6F 6E 00 00 00 00 00 00 00 00 00 00 00 09 04 0C 00 78 03 01 00 00 01 00 7F 00 01 00 00 02 00 00 00 32 32 00 32 00 00 00 00 00 00 10 0A 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 00 04 00 00 00 01 00 00 00 24 00 10 01 0E 25 01 11 01 0E 26 02 12 01 0E 27 03 13 01 0E 28 04 14 01 0E 29 05 15 01 0E 2A 06 16 01 0E 2B 07 17 01 0E 2C 08 18 01 0E 2D 09 19 01 0E 2E 0A 1A 01 0E 2F 0B 1B 01 0E 30 0C 1C 01 0E 31 0D 1D 01 0E 32 0E 1E 01 0E 33 0F 1F 01 0E 18 00 7F 00 4B 6E 6F 62 31 00 00 00 00 00 00 00 00 00 00 00 19 00 7F 00 4B 6E 6F 62 32 00 00 00 00 00 00 00 00 00 00 00 1A 00 7F 00 4B 6E 6F 62 33 00 00 00 00 00 00 00 00 00 00 00 1B 00 7F 00 4B 6E 6F 62 34 00 00 00 00 00 00 00 00 00 00 00 1C 00 7F 00 4B 6E 6F 62 35 00 00 00 00 00 00 00 00 00 00 00 1D 00 7F 00 4B 6E 6F 62 36 00 00 00 00 00 00 00 00 00 00 00 1E 00 7F 00 4B 6E 6F 62 37 00 00 00 00 00 00 00 00 00 00 00 1F 00 7F 00 4B 6E 6F 62 38 00 00 00 00 00 00 00 00 00 00 00 F7"),
    }
end

function remote_process_midi(event)
    -- Channel 10 notes (pads) pass through to auto_inputs -> Keyboard
    -- Don't intercept them here - let keyboard patterns handle them

    -- Transport CC handling - only process events from DAW Port (port=1)
    -- Note: event.port is 1-indexed in Reason Remote
    if event.port == 1 then
        local ret = remote.match_midi("b0 xx yy", event)
        if ret then
            local cc = ret.x
            local value = ret.y

            -- CC 76 = Play/Stop toggle button
            if cc == 0x4c and value > 0 then
                g_is_playing = not g_is_playing
                if g_is_playing then
                    remote.handle_input({ time_stamp=event.time_stamp, item=g_items["Play"], value=1 })
                else
                    remote.handle_input({ time_stamp=event.time_stamp, item=g_items["Stop"], value=1 })
                end
                return true
            end

            -- CC 17 = SHIFT button
            if cc == 0x11 then
                g_shift_held = (value > 0)
                return true
            end

            -- CC 77 = Record button (or Quantize when SHIFT held)
            if cc == 0x4d and value > 0 then
                if g_shift_held then
                    remote.handle_input({ time_stamp=event.time_stamp, item=g_items["Quantize"], value=1 })
                else
                    remote.handle_input({ time_stamp=event.time_stamp, item=g_items["Record"], value=1 })
                end
                return true
            end

            -- CC 73 = Undo button (or Redo when SHIFT held)
            if cc == 0x49 and value > 0 then
                if g_shift_held then
                    remote.handle_input({ time_stamp=event.time_stamp, item=g_items["Redo"], value=1 })
                else
                    remote.handle_input({ time_stamp=event.time_stamp, item=g_items["Undo"], value=1 })
                end
                return true
            end

            -- CC 11 = Tap Tempo button (or Click when SHIFT held)
            if cc == 0x0b then
                if g_shift_held and value > 0 then
                    remote.handle_input({ time_stamp=event.time_stamp, item=g_items["Click"], value=1 })
                else
                    remote.handle_input({ time_stamp=event.time_stamp, item=g_items["Tap Tempo"], value=value })
                end
                return true
            end
        end
    end

    return false
end

function remote_set_state(changed_items)
    -- Track transport state from Reason
    if g_items and g_items["Play"] then
        for i, item_index in ipairs(changed_items) do
            if item_index == g_items["Play"] then
                local state = remote.get_item_state(item_index)
                if state and state.value then
                    g_is_playing = (state.value > 0)
                end
            end
        end
    end
end
