local CyberhackLayer = {}
local show_helps = false

local offset = 27
local size = 54
	
function Split(s, delimiter)
    result = {}
	if s == nil then
		return result
	end
    for match in (s..delimiter):gmatch("(.-)"..delimiter) do
        table.insert(result, match);
    end
    return result;
end


registerForEvent('onInit', function()
	print("Init complete")
end)

function UpdateCmds()
	if show_helps then
		show_helps = false
	else
		file = io.open("cmd.txt", "w")
		file:write("+")
		file:close()
		show_helps = true
	end
end

local hit_number = 0
local prev_hit_x = 0
local prev_hit_y = 0

function DrawItem(item)
	local dl = ImGui.GetForegroundDrawList()
	cmd = Split(item, ";")
	if table.getn(cmd) > 1 then
		oper_type = cmd[1]
		
		if oper_type == "hit" then
			text = cmd[2]
			x = tonumber(cmd[3])
			y = tonumber(cmd[4])
			color = tonumber(cmd[5])
			ImGui.ImDrawListAddCircle(dl, x, y, offset, color, 6, 2.0)
			ImGui.ImDrawListAddText(dl, x - offset, y - offset, color, text)
			if hit_number > 0 then
				local lx = 0
				local ly = 0
				local dx = prev_hit_x - x
				local dy = prev_hit_y - y
				if dx > offset then lx = offset end
				if dx < -offset then lx = -offset end
				
				if dy > offset then ly = offset end
				if dy < -offset then ly = -offset end
				
				ImGui.ImDrawListAddLine(dl, prev_hit_x - lx, prev_hit_y - ly, x + lx, y + ly, color, 4)
			end
			prev_hit_x = x
			prev_hit_y = y
			hit_number = hit_number + 1
		end
		
		if oper_type == "text" then
			text = cmd[2]
			x = tonumber(cmd[3])
			y = tonumber(cmd[4])
			color = tonumber(cmd[5])
			ImGui.ImDrawListAddText(dl, x, y, color, text)
		end
	end
end

function DrawOverlay()
	hit_number = 0
	file = io.open("clickmap.txt", "r")
	lines = file:lines()
	local id = 1
	
	for line in lines do
		if line:len() > 1 then
			DrawItem(line)
		end
	end 
	file:close()
end

registerForEvent('onDraw', function()
	DrawOverlay()
end)

return CyberhackLayer