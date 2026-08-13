# install.ps1: Windows installer; mirrors adapters/install.sh.
# The host list is read from registries/hosts.json (no hardcoded tool list).
#
# Usage:
#   ./install.ps1 -Action install              # link all adapters (default)
#   ./install.ps1 -Action uninstall
#   ./install.ps1 -Action status
#   ./install.ps1 -Action list
#   ./install.ps1 -Action install -Tool claude # one adapter
#   ./install.ps1 -Action install -DryRun      # preview
#   ./install.ps1 -Action install -Force       # replace stale symlinks
[CmdletBinding()]
param(
  [ValidateSet('install', 'uninstall', 'status', 'list')]
  [string]$Action = 'install',
  [string]$Tool = '',
  [switch]$DryRun,
  [switch]$Force
)

$ErrorActionPreference = 'Stop'
$RepoDir = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$HostsReg = Join-Path $RepoDir 'registries\hosts.json'
$Doctrine = 'AGENTS.md'

if (-not (Test-Path $HostsReg)) { throw "registry not found: $HostsReg" }
$reg = Get-Content $HostsReg -Raw | ConvertFrom-Json

function Expand-Home($p) { return $p -replace '\$HOME', $HOME }

function Link-Artifact($src, $dest, $label) {
  if (Test-Path $dest) {
    $item = Get-Item $dest -Force
    if ($item.LinkType -eq 'SymbolicLink') {
      if ($Force) {
        if ($DryRun) { Write-Host "  ($label) replace link $dest" } else { Remove-Item $dest }
      } elseif ((Resolve-Path $item.Target -ErrorAction SilentlyContinue) -eq (Resolve-Path $src -ErrorAction SilentlyContinue)) {
        Write-Host "  ($label) already linked"; return
      } else {
        Write-Host "  ($label) SKIP: $dest links elsewhere (use -Force)"; return
      }
    } else {
      Write-Host "  ($label) SKIP: $dest is real (not clobbered)"; return
    }
  }
  if ($DryRun) { Write-Host "  ($label) link $dest -> $src" }
  else { $null = New-Item -ItemType SymbolicLink -Path $dest -Target $src -Force; Write-Host "  ($label) linked $dest" }
}

function Unlink-Artifact($dest, $label) {
  if (Test-Path $dest) {
    $item = Get-Item $dest -Force
    if ($item.LinkType -eq 'SymbolicLink') {
      if ($DryRun) { Write-Host "  ($label) remove $dest" } else { Remove-Item $dest }
      Write-Host "  ($label) removed $dest"
    } else { Write-Host "  ($label) SKIP: $dest is real" }
  } else { Write-Host "  ($label) absent" }
}

function Status-Artifact($src, $dest, $label) {
  if (Test-Path $dest) {
    $item = Get-Item $dest -Force
    if ($item.LinkType -eq 'SymbolicLink') {
      $t = (Resolve-Path $item.Target -ErrorAction SilentlyContinue)
      if ($t -and ($t -eq (Resolve-Path $src -ErrorAction SilentlyContinue))) { Write-Host "  ($label) OK -> $src" }
      else { Write-Host "  ($label) STALE -> $($item.Target)" }
    } else { Write-Host "  ($label) REAL-FILE at $dest" }
  } else { Write-Host "  ($label) not installed" }
}

if ($Action -eq 'list') {
  Write-Host "Adapters from registries/hosts.json:"
  foreach ($a in $reg.adapters) {
    $extra = if ($a.surfaces.agents) { " agents->$($a.surfaces.agents_path)" } else { '' }
    Write-Host ("  {0,-16} {1}  ({2}){3}" -f $a.code, $a.config_dir, $a.config_file, $extra)
  }
  return
}

Write-Host "mode=$Action dry-run=$DryRun force=$Force$(if ($Tool) { " filter=$Tool" })"

foreach ($a in $reg.adapters) {
  if ($Tool -and $a.code -ne $Tool) { continue }
  $dir = Expand-Home $a.config_dir
  Write-Host "[$($a.code)] -> $dir"
  switch ($Action) {
    'install' {
      Link-Artifact (Join-Path $RepoDir $Doctrine) (Join-Path $dir $a.config_file) 'doctrine'
      if ($a.surfaces.skills)  { Link-Artifact (Join-Path $RepoDir 'skills') (Join-Path $dir 'skills') 'skills' }
      if ($a.surfaces.commands){ Link-Artifact (Join-Path $RepoDir 'commands') (Join-Path $dir 'commands') 'commands' }
      if ($a.surfaces.agents -and $a.surfaces.agents_path) { Link-Artifact (Join-Path $RepoDir 'agents') (Join-Path $dir $a.surfaces.agents_path) 'agents' }
    }
    'uninstall' {
      Unlink-Artifact (Join-Path $dir $a.config_file) 'doctrine'
      if ($a.surfaces.skills)  { Unlink-Artifact (Join-Path $dir 'skills') 'skills' }
      if ($a.surfaces.commands){ Unlink-Artifact (Join-Path $dir 'commands') 'commands' }
      if ($a.surfaces.agents -and $a.surfaces.agents_path) { Unlink-Artifact (Join-Path $dir $a.surfaces.agents_path) 'agents' }
    }
    'status' {
      Status-Artifact (Join-Path $RepoDir $Doctrine) (Join-Path $dir $a.config_file) 'doctrine'
      if ($a.surfaces.skills)  { Status-Artifact (Join-Path $RepoDir 'skills') (Join-Path $dir 'skills') 'skills' }
      if ($a.surfaces.commands){ Status-Artifact (Join-Path $RepoDir 'commands') (Join-Path $dir 'commands') 'commands' }
      if ($a.surfaces.agents -and $a.surfaces.agents_path) { Status-Artifact (Join-Path $RepoDir 'agents') (Join-Path $dir $a.surfaces.agents_path) 'agents' }
    }
  }
}

if ($DryRun) { Write-Host "(--dry-run: no filesystem changes were made)" }
