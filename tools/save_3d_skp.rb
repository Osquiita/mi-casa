# -*- coding: utf-8 -*-
model = Sketchup.active_model
dir = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/modelo-3d"
require "fileutils"
FileUtils.mkdir_p(dir)

out1 = "C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp"
out2 = "#{dir}/casa-bifamiliar-2025.skp"

FileUtils.rm_f(out1) if File.exist?(out1)
FileUtils.rm_f(out2) if File.exist?(out2)

s1 = model.save(out1)
s2 = model.save(out2)

"SKP GUARDADO: #{s1} -> #{out1} | #{s2} -> #{out2}"