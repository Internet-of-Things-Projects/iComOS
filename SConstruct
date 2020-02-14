#===============================================================================
# @brief    Scons make file
# Copyright (c) 2016 NEUL LIMITED
#===============================================================================

import os
import sys
import subprocess

DefaultEnvironment(tools=[])

sys.path.append(os.path.realpath('tools'))
sys.path.append(os.path.join('tools', 'SCons'))
import ModuleUtils
from EnvironmentUtils import NeulBuildConfig, NeulTargetConfig, BuildType
from arm_tools import install_arm_tools
from common_tools import install_common_tools
from scons_targets.scons_targets import configs, aliases


#===============================================================================
# Function definitions
#===============================================================================

def install_spawn(env):
    """
    Install a new SPAWN function for creating processes. We prefer to go direct
    without going via the shell, as Windows has a length restriction on its
    command line.
    """
    # This code is from the SCons Wiki: https://bitbucket.org/scons/scons/wiki/LongCmdLinesOnWin32
    if env['PLATFORM'] == 'win32':
        old_spawn = env['SPAWN']

        def my_spawn(sh, escape, cmd, args, spawnenv):
            # If we're trying to use redirection, just use the original one and hope there isn't also
            # a long command line.
            if ">" in args:
                return old_spawn(sh, escape, cmd, args, spawnenv)

            newargs = ' '.join(args[1:])
            cmdline = cmd + " " + newargs
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            proc = subprocess.Popen(cmdline, startupinfo=startupinfo, shell = False, env = spawnenv)
            rv = proc.wait()
            return rv

        env['SPAWN'] = my_spawn

def add_rpc_code(env, rpc_path):
    env['rpc_core'] = 'application'
    env.Append(CPPPATH = [os.path.join(rpc_path, 'public', 'application')])


def build(config, args):
    # Update config specific build information. Required for get_build_dir, below.
    NeulBuildConfig.set_build_info(config)

    # Create environment, using SYSTEM PATH, and GNU toolchain!
    environment_vars = {'PATH' : os.environ['PATH'],
                'SYSTEMROOT' : os.environ["SYSTEMROOT"],
              }
    if os.environ.has_key("ECLIPSE_DIR"):
        environment_vars["ECLIPSE_DIR"] = os.environ["ECLIPSE_DIR"]

    env = Environment(
        ENV = environment_vars,
        tools = ['gcc', 'g++', 'gas', 'ar', 'gnulink'], 
    )
    
    # Set authentication assets to use
    asset_args = ARGUMENTS.get('sign_asset', None)
    NeulTargetConfig.set_build_info_per_target(config, env, asset_args)

    # Install spawn function to cope with long command lines.
    install_spawn(env)

    # Perform build-specific actions here
    if NeulTargetConfig.get_build_type(env) == BuildType.ARM:
        install_arm_tools(env, NeulBuildConfig)
    
    install_common_tools(env)

    # Pretty-fy the output.
    if int(ARGUMENTS.get('VERBOSE', 0)) == 0:
        env['ASCOMSTR'] = 'Compiling asm $SOURCE ...'
        env['ASPPCOMSTR'] = 'Compiling preprocessed asm $SOURCE ... '
        env['ARCOMSTR'] = 'Linking $TARGET ...'
        env['CCCOMSTR'] = 'Compiling $SOURCE ...'
        env['CXXCOMSTR'] = 'Compiling $SOURCE ...'
        env['LINKCOMSTR'] = 'Linking $TARGET ...'
        env['RANLIBCOMSTR'] = 'Indexing $TARGET ...'
        
        env['SHCCCOMSTR'] = 'Compiling $SOURCE ...'
        env['SHCXXCCOMSTR'] = 'Compiling $SOURCE ...'
        env['SHLINKCOMSTR'] = 'Linking $TARGET ...'
        
        env['PCLINT_COMSTR'] = 'Linting $SOURCES ...'
        env['PCLINT_LIB_COMSTR'] = 'Linting $SOURCES ...'
    
    if int(ARGUMENTS.get('DEBUG', 1)) == 1:
        env.Append(CCFLAGS = [ '-g' ])
        env.Append(LINKFLAGS = [ '-g' ])
        env.Append(ASFLAGS = [ '-g' ])
        
    env.Append(ASFLAGS = [ '-c' ])
    
    for key, value in ARGLIST:
        if key == 'def':
            print "Appending %s" % value
            env.Append(CPPDEFINES = [value]) 

    env.Append(CPPDEFINES = "TARGET_CHIP_" + config['chip'].upper())

    # Recurse into src, passing the above environment (and tools), without copying the source!
    return SConscript(os.path.join('src', 'SConscript'), {'env' : env}, variant_dir = NeulTargetConfig.get_build_dir(env), duplicate = 0)


def check_target(target):
    if configs.has_key(target):
        print 'Check target  "%s"' % (target)
        build(configs[target], ARGUMENTS)
        print("Check target ok")
        return True
    else:
        return False
        
def check_alias(target):
    if aliases.has_key(target):
        for t in aliases[target]:
            # Handle ALIAS within ALIAS recursion...
            if aliases.has_key(t):
                check_alias(t)
            else:
                print 'check alias "%s"' % (target)
                build(configs[t], ARGUMENTS)
        return True
    else:
        return False
        
#===============================================================================
# Main process
#===============================================================================

for target in ARGUMENTS.get('target', '').split(','):

    # First check for REAL targets
    target = target.lower()
    if check_target(target):
        pass
    # Then check for ALIASES (recursive)
    elif check_alias(target):
        pass
    else:
        if target == '': 
            print 'No target specified.'
        else:
            print 'Specified target \"%s\" is not valid.' % target
        print '\r\n' + 'List of targets:'
        keylist = configs.keys()
        keylist.sort()
        for t in keylist:
            print t
        print '\r\n' + 'List of aliases:'
        keylist = aliases.keys()
        keylist.sort()
        for t in keylist:
            print t
        print
        sys.exit(1)

