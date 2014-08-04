[Mesh]
  type = FileMesh
  file = mug.e
[]

[Variables]
  [./convected]
    order = FIRST
    family = LAGRANGE
  [../]
[]

[Kernels]
  [./diff]
    type = Diffusion
    variable = convected
  [../]
  [./conv]
    type = Convection
    variable = convected
    velocity = '0.0 0.0 1.0'
  [../]
[]

[BCs]
  [./bottom]
    type = DirichletBC
    variable = convected
    boundary = bottom
    value = 1
  [../]
  [./top]
    type = DirichletBC
    variable = convected
    boundary = top
    value = 0
  [../]
[]

[Executioner]
  # Preconditioned JFNK (default)
  type = Steady
  solve_type = PJFNK
[]

[Outputs]
  file_base = out
  exodus = true
  [./console]
    type = Console
    perf_log = true
    linear_residuals = true
  [../]
[]

