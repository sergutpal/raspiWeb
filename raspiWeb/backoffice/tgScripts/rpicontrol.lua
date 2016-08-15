started = 0
our_id = 0
path = "/home/nfs/telegram/tgScripts"
SERGIO = "Sergio"
IRINA = "Irina"
CAOC = "CAOC"

function vardump(value, depth, key)
  local linePrefix = ""
  local spaces = ""

  if key ~= nil then
    linePrefix = "["..key.."] = "
  end

  if depth == nil then
    depth = 0
  else
    depth = depth + 1
    for i=1, depth do spaces = spaces .. "  " end
  end

  if type(value) == 'table' then
    mTable = getmetatable(value)
    if mTable == nil then
      print(spaces ..linePrefix.."(table) ")
    else
      print(spaces .."(metatable) ")
        value = mTable
    end
    for tableKey, tableValue in pairs(value) do
      vardump(tableValue, depth, tableKey)
    end
  elseif type(value)	== 'function' or
      type(value)	== 'thread' or
      type(value)	== 'userdata' or
      value		== nil
  then
    print(spaces..tostring(value))
  else
    print(spaces..linePrefix.."("..type(value)..") "..tostring(value))
  end
end

-- print ("Controlador rpicontrol.lua en ejecucion")

function ok_cb(extra, success, result)
 	print ("soy ok_cb")
end

-- Notification code {{{

function get_title (P, Q)
  if (Q.type == 'user') then
    return P.first_name .. " " .. P.last_name
  elseif (Q.type == 'chat') then
    return Q.title
  elseif (Q.type == 'encr_chat') then
    return 'Secret chat with ' .. P.first_name .. ' ' .. P.last_name
  else
    return ''
  end
end

local lgi = require ('lgi')
local notify = lgi.require('Notify')
notify.init ("Telegram updates")
local icon = path .. "/icon.png"

function do_notify (user, msg)
  local n = notify.Notification.new(user, msg, icon)
  n:show ()
end

-- }}}

function file_exists(name)
	local f=io.open(name,"r")
	if f~=nil then
		io.close(f)
		return true
	else
		return false
	end
end

function split(inputstr, sep)
        if sep == nil then
                sep = "%s"
        end
        local t={} ;
        t[1] = 0
        z = 2
        for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
                t[z] = str
                z = z + 1
        end
        t[1] = z -1
        return t
end

function on_msg_receive (msg)
  if started == 0 then
    return
  end
  if msg.out then
    return
  end

  if msg.text ==nil then
    return
  end

  -- do_notify (get_title (msg.from, msg.to), msg.text)

  msgFrom = msg.from.print_name
  if (msgFrom ==SERGIO) or (msgFrom ==IRINA) or (msgFrom ==CAOC) then
        local msgFull =string.lower(msg.text)
        print('MENSAJE RECIBIDO de '..msgFrom..': #'..msgFull..'#')
        local msgSplit =split(msgFull)
        local msgText =msgSplit[2]
        local msgParam1 =msgSplit[3]
        local msgParam2 =msgSplit[4]
        local msgParams =''
        if msgParam1 ~=nil then
          msgParams = ' '..msgParam1
        end
        if msgParam2 ~=nil then
          msgParams = msgParams..' '..msgParam2
        end
	if file_exists(path..'/'..msgText..'.py') then
                local cmd = 'python '..path..'/'..msgText..'.py'..msgParams
                print('EJECUTANDO CMD: #'..cmd..'#')
		os.execute(cmd)
		return
	end
  end
end

function on_our_id (id)
  our_id = id
end

function on_user_update (user, what)
  --vardump (user)
end

function on_chat_update (chat, what)
  --vardump (chat)
end

function on_secret_chat_update (schat, what)
  --vardump (schat)
end

function on_get_difference_end ()
end

function cron()
  -- do something
  postpone (cron, false, 1.0)
end

function on_binlog_replay_end ()
  started = 1
  postpone (cron, false, 1.0)
end
