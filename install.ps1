# install.ps1  --  install this repo as a plugin into supported AI tools (Windows).
#
# Companion to link.sh / install.sh. Same plugin-marketplace semantics
# (link AGENTS.md, commands/, skills/, agents/ into each detected tool's
# config dir using the tool-specific filename and agents dir).
#
# PowerShell 5.1+ compatible. Uses New-Item -ItemType SymbolicLink,
# which works without admin rights for paths inside the user profile.
#
# Syntax:
#   install.ps1 -Action install            # link all detected tools (default)
#   install.ps1 -Action uninstall          # remove the symlinks
#   install.ps1 -Action status             # show current linkage state
#   install.ps1 -Action list               # list detected tools + target paths
#
# Options:
#   -Tool <name>     apply the action to one tool only
#   -DryRun          print actions without executing
#   -Force           replace a stale symlink (never overwrite a real file/dir)
#   -Help            show usage
#
# Tools supported (mirror link.sh / install.sh exactly):
#   gemini, antigravity, antigravity-ide  ->  $HOME\.gemini\GEMINI.md
#   codex                                  ->  $HOME\.codex\AGENTS.md
#   claude                                 ->  $HOME\.claude\CLAUDE.md
#   qwen                                   ->  $HOME\.qwen\AGENTS.md
#   opencode                               ->  $HOME\.config\opencode\AGENTS.md  (agents dir: agents\)
#   kilo                                   ->  $HOME\.config\kilo\AGENTS.md      (agents dir: agent\)
#
[CmdletBinding()]
param(
    [ValidateSet('install','uninstall','status','list')]
    [string]$Action = 'install',

    [ValidateSet('gemini','antigravity','antigravity-ide','codex','claude','qwen','opencode','kilo','')]
    [string]$Tool = '',

    [switch]$DryRun,
    [switch]$Force,
    [switch]$Help
)

$ErrorActionPreference = 'Stop'
$REPO_DIR = (Resolve-Path -LiteralPath $PSScriptRoot).ProviderPath

if ($Help) {
    @'
Usage: install.ps1 -Action <install|uninstall|status|list> [-Tool <name>] [-DryRun] [-Force] [-Help]

Modes:
  install     link plugin artifacts into every detected tool (default)
  uninstall   remove the symlinks previously created
  status      show current linkage state for detected tools
  list        list detected tools and their target paths (no changes)

Options:
  -Tool <name>  apply the action to one tool only
              (gemini, antigravity, antigravity-ide, codex, claude, qwen, opencode, kilo)
  -DryRun       print actions without executing them
  -Force        replace a stale symlink (never overwrite a real file/dir)
  -Help         show this message
'@
    exit 0
}

# Build the tool table in a fixed order, matching install.sh.
$TARGETS = @(
    @{ Name='gemini';          Dir=("$HOME\.gemini");              AgentFile='GEMINI.md'; AgentsDir=''  }
    @{ Name='antigravity';     Dir=("$HOME\.gemini");              AgentFile='GEMINI.md'; AgentsDir=''  }
    @{ Name='antigravity-ide'; Dir=("$HOME\.gemini");              AgentFile='GEMINI.md'; AgentsDir=''  }
    @{ Name='codex';           Dir=("$HOME\.codex");               AgentFile='AGENTS.md'; AgentsDir=''  }
    @{ Name='claude';          Dir=("$HOME\.claude");              AgentFile='CLAUDE.md'; AgentsDir=''  }
    @{ Name='qwen';            Dir=("$HOME\.qwen");                AgentFile='AGENTS.md'; AgentsDir=''  }
    @{ Name='opencode';        Dir=("$HOME\.config\opencode");    AgentFile='AGENTS.md'; AgentsDir='agents' }
    @{ Name='kilo';            Dir=("$HOME\.config\kilo");         AgentFile='AGENTS.md'; AgentsDir='agent'  }
)

$PLUGIN_FILE = 'AGENTS.md'
$PLUGIN_DIRS = @('commands', 'skills')
$PLUGIN_AGENTS_DIR = 'agents'

function Write-Log {
    Param([string]$Message)
    Write-Host "[install] $Message"
}

function Write-Warn {
    Param([string]$Message)
    Microsoft.PowerShell.Utility\Write-Warning "[install] $Message"
}

function Write-Dry {
    Param([string]$Message)
    Write-Host "[install] (dry-run) $Message"
}

function Format-LinkTargetPath([string]$dir, [string]$name) {
    return (Join-Path -Path $dir -ChildPath $name)
}

function Get-LinkStatus {
    Param([string]$Path)
    if (Test-Path -LiteralPath $Path) {
        $item = Get-Item -LiteralPath $Path -Force
        if ($item.Attributes.HasFlag([IO.FileAttributes]::ReparsePoint)) {
            return 'symlink'
        }
        return 'real'
    }
    return 'missing'
}

function Link-Artifact {
    Param([string]$Src, [string]$Dst, [string]$Label)

    if (-not (Test-Path -LiteralPath $Src)) {
        Write-Warn "source $Src missing -- cannot link"
        return 1
    }

    $dstExists = Test-Path -LiteralPath $Dst
    if ($dstExists) {
        $status = Get-LinkStatus -Path $Dst
        if ($status -eq 'symlink') {
            $current = (Get-Item -LiteralPath $Dst -Force).Target
            $resolved = $Src
            try { $resolved = (Resolve-Path -LiteralPath $Src).ProviderPath } catch { }
            if ($current -eq $resolved -or $current -eq $Src) {
                Write-Log "tool already linked ($Label)"
                return 0
            }
            if ($Force) {
                if ($DryRun) {
                    Write-Dry "replace stale symlink $Dst (currently -> $current) -> $Src"
                }
                else {
                    Remove-Item -LiteralPath $Dst -Force
                    New-Item -ItemType SymbolicLink -Path $Dst -Target $Src | Out-Null
                }
                Write-Log "linked $Dst -> $Src"
                return 0
            }
            Write-Warn "$Dst is a symlink to $current (not $Src); pass -Force to replace"
            return 1
        }
        Write-Warn "$Dst exists as a real file/directory -- skipping to avoid data loss"
        return 1
    }

    $parent = Split-Path -Parent -Path $Dst
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    if ($DryRun) {
        Write-Dry "link $Dst -> $Src"
    }
    else {
        New-Item -ItemType SymbolicLink -Path $Dst -Target $Src | Out-Null
    }
    Write-Log "linked $Dst -> $Src"
    return 0
}

function Unlink-Artifact {
    Param([string]$Dst)

    if (Test-Path -LiteralPath $Dst) {
        $status = Get-LinkStatus -Path $Dst
        if ($status -eq 'symlink') {
            if ($DryRun) {
                Write-Dry "remove symlink $Dst (-> $((Get-Item -LiteralPath $Dst -Force).Target))"
            }
            else {
                Remove-Item -LiteralPath $Dst -Force
                Write-Log "removed $Dst"
            }
            return
        }
        Write-Warn "$Dst exists but is not a symlink -- leaving alone"
    }
}

function Show-ArtifactStatus {
    Param([string]$Src, [string]$Dst)

    if (Test-Path -LiteralPath $Dst) {
        $status = Get-LinkStatus -Path $Dst
        if ($status -eq 'symlink') {
            $current = (Get-Item -LiteralPath $Dst -Force).Target
            if ($current -eq $Src) {
                Write-Host "  OK    $Dst"
                return
            }
            Write-Host "  ??    $Dst -> $current (expected $Src)"
            return
        }
        Write-Host "  !!    $Dst exists but is not a symlink"
        return
    }
    Write-Host "  --    $Dst (not linked)"
}

function Invoke-InstallTool {
    Param([hashtable]$Target)

    $name      = $Target.Name
    $dir       = $Target.Dir
    $agentFile = $Target.AgentFile
    $agentsDir = $Target.AgentsDir

    if (-not (Test-Path -LiteralPath $dir)) {
        Write-Log "$dir does not exist -- skipping $name"
        return @{ Updated=0; Skipped=0; Detected=$false }
    }

    $updated = 0
    $skipped = 0

    if ($DryRun) { Write-Dry "tool $name : would link into $dir" }
    else         { Write-Log "tool $name : linking into $dir" }

    $cfgDst = Format-LinkTargetPath $dir $agentFile
    if ((Link-Artifact -Src (Join-Path $REPO_DIR $PLUGIN_FILE) -Dst $cfgDst -Label 'config') -eq 0) { $updated++ } else { $skipped++ }

    foreach ($d in $PLUGIN_DIRS) {
        $subDst = Format-LinkTargetPath $dir $d
        if ((Link-Artifact -Src (Join-Path $REPO_DIR $d) -Dst $subDst -Label "$d/") -eq 0) { $updated++ } else { $skipped++ }
    }

    if (-not [string]::IsNullOrEmpty($agentsDir)) {
        $aDst = Format-LinkTargetPath $dir $agentsDir
        if ((Link-Artifact -Src (Join-Path $REPO_DIR $PLUGIN_AGENTS_DIR) -Dst $aDst -Label 'agents/') -eq 0) { $updated++ } else { $skipped++ }
    }

    return @{ Updated=$updated; Skipped=$skipped; Detected=$true }
}

function Invoke-UninstallTool {
    Param([hashtable]$Target)

    $name      = $Target.Name
    $dir       = $Target.Dir
    $agentFile = $Target.AgentFile
    $agentsDir = $Target.AgentsDir

    if (-not (Test-Path -LiteralPath $dir)) {
        Write-Log "$dir does not exist -- nothing to remove for $name"
        return
    }

    Write-Log "tool $name : removing links from $dir"

    Unlink-Artifact -Dst (Format-LinkTargetPath $dir $agentFile)
    foreach ($d in $PLUGIN_DIRS) {
        Unlink-Artifact -Dst (Format-LinkTargetPath $dir $d)
    }
    if (-not [string]::IsNullOrEmpty($agentsDir)) {
        Unlink-Artifact -Dst (Format-LinkTargetPath $dir $agentsDir)
    }
}

function Show-StatusTool {
    Param([hashtable]$Target)

    $name      = $Target.Name
    $dir       = $Target.Dir
    $agentFile = $Target.AgentFile
    $agentsDir = $Target.AgentsDir

    Write-Host "[$name]"

    if (-not (Test-Path -LiteralPath $dir)) {
        Write-Host "  --    $dir (config directory does not exist)"
        return
    }

    Show-ArtifactStatus -Src (Join-Path $REPO_DIR $PLUGIN_FILE) -Dst (Format-LinkTargetPath $dir $agentFile)
    foreach ($d in $PLUGIN_DIRS) {
        Show-ArtifactStatus -Src (Join-Path $REPO_DIR $d) -Dst (Format-LinkTargetPath $dir $d)
    }
    if (-not [string]::IsNullOrEmpty($agentsDir)) {
        Show-ArtifactStatus -Src (Join-Path $REPO_DIR $PLUGIN_AGENTS_DIR) -Dst (Format-LinkTargetPath $dir $agentsDir)
    }
}

function Show-ListTool {
    Param([hashtable]$Target)

    $name      = $Target.Name
    $dir       = $Target.Dir
    $agentFile = $Target.AgentFile
    $agentsDir = $Target.AgentsDir

    $present = if (Test-Path -LiteralPath $dir) { 'yes' } else { 'no' }
    $line = "  {0,-18}  config={1}  config_file={2,-12}  detected={3}" -f $name, $dir, $agentFile, $present
    if (-not [string]::IsNullOrEmpty($agentsDir)) {
        $line += "  agents_dir=$agentsDir"
    }
    Write-Host $line
}

$UPDATED = 0
$SKIPPED = 0
$DETECTED = 0

foreach ($target in $TARGETS) {
    if (-not [string]::IsNullOrEmpty($Tool) -and $target.Name -ne $Tool) {
        continue
    }

    switch ($Action) {
        'list' {
            Show-ListTool -Target $target
            if (Test-Path -LiteralPath $target.Dir) { $DETECTED++ }
        }
        'install' {
            $r = Invoke-InstallTool -Target $target
            $UPDATED += $r.Updated
            $SKIPPED += $r.Skipped
            if ($r.Detected) { $DETECTED++ }
        }
        'uninstall' {
            Invoke-UninstallTool -Target $target
        }
        'status' {
            Show-StatusTool -Target $target
            if (Test-Path -LiteralPath $target.Dir) { $DETECTED++ }
        }
    }
}

switch ($Action) {
    'list' {
        Write-Host ""
        if ($DETECTED -eq 0) {
            Write-Host "no tools detected (none of the supported config directories exist on this machine)"
        }
        else {
            Write-Host ""
            Write-Host "$DETECTED tool(s) detected"
        }
    }
    'install' {
        Write-Host ""
        Write-Log "summary: $UPDATED artifact(s) updated, $SKIPPED skipped across $DETECTED tool(s) detected"
        if ($Force)   { Write-Log "(-Force enabled: stale symlinks were replaced)" }
        if ($DryRun)  { Write-Log "(-DryRun: no filesystem changes were made)" }
    }
    'uninstall' {
        Write-Log "summary: uninstall finished; pass '-Action status' to verify"
        if ($DryRun) { Write-Log "(-DryRun: no filesystem changes were made)" }
    }
    'status' { }
}

exit 0
