@echo off
REM ====About this POST-COMMIT HOOK script===========================

:: This script is expected to be executed after commit being completed
:: Then it uses "svnlook" command to collect information regarding to this commit
:: After writing above information into "message.txt", the EmailSender.py will send the content
:: of this file to every Email Address listed in EmailSenderConfig.xml

:: This scripts should be located in the [repository_path]\hooks

REM ====About POST-COMMIT HOOK=================================

:: POST-COMMIT HOOK
::
:: The post-commit hook is invoked after a commit.  Subversion runs
:: this hook by invoking a program (script, executable, binary, etc.)
:: named 'post-commit' (for which this file is a template) with the 
:: following ordered arguments:
::
::   [1] REPOS-PATH   (the path to this repository)
::   [2] REV          (the number of the revision just committed)
::   [3] TXN-NAME     (the name of the transaction that has become REV)
::
:: The default working directory for the invocation is undefined, so
:: the program should set one explicitly if it cares.
::
:: Because the commit has already completed and cannot be undone,
:: the exit code of the hook program is ignored.  The hook program
:: can use the 'svnlook' utility to help it examine the
:: newly-committed tree.
::
:: On a Unix system, the normal procedure is to have 'post-commit'
:: invoke other programs to do the real work, though it may do the
:: work itself too.
::
:: Note that 'post-commit' must be executable by the user(s) who will
:: invoke it (typically the user httpd runs as), and that user must
:: have filesystem-level permission to access the repository.
::
:: On a Windows system, you should name the hook program
:: 'post-commit.bat' or 'post-commit.exe',
:: but the basic idea is the same.
:: 
:: The hook program typically does not inherit the environment of
:: its parent process.  For example, a common problem is for the
:: PATH environment variable to not be set to its usual value, so
:: that subprograms fail to launch unless invoked via absolute path.
:: If you're having unexpected problems with a hook program, the
:: culprit may be unusual (or missing) environment variables.
:: 
:: Here is an example hook script, for a Unix /bin/sh interpreter.
:: For more examples and pre-written hooks, see those in
:: the Subversion repository at
:: http://svn.apache.org/repos/asf/subversion/trunk/tools/hook-scripts/ and
:: http://svn.apache.org/repos/asf/subversion/trunk/contrib/hook-scripts/

REM ==============================================


setlocal
REM D:\SVN_TEST\data\repositories\test2  
REM D:\SVN_TEST\data\repositories\test2\Email\message.txt

set REPOS=%1
set REV=%2
set TXN_NAME=%3
set OutputFile=./Email/message.txt

echo The SVN Post-Commit Email > %OutputFile%
set <nul /p=Date:	>> %OutputFile% & date /t >> %OutputFile%
set <nul /p=Time:	>> %OutputFile% & time /t >> %OutputFile%
echo *********************************************************************************************************** >> %OutputFile%
REM echo *********************************************************************************************************** >> %OutputFile%

echo.  >> %OutputFile%
echo Repository:      %REPOS% >> %OutputFile%
echo Revision:        %REV% >> %OutputFile%
echo Transaction:     %TXN_NAME% >> %OutputFile%
echo *********************************************************************************************************** >> %OutputFile%
REM echo *********************************************************************************************************** >> %OutputFile%

for /f "delims=" %%i in ('svnlook author %REPOS% -r %REV%') do @set svn_author=%%i 
for /f "delims=" %%i in ('svnlook date %REPOS% -r %REV%') do @set svn_date=%%i 
REM for /f "delims=" %%i in ('svnlook log %REPOS% -r %REV%') do @set svn_log=%%i 
REM for /f "delims=" %%i in ('svnlook changed %REPOS% -r %REV%') do @set svn_changed=%%i
REM for /f "delims=" %%i in ('svnlook diff %REPOS% -r %REV%') do @set svn_diff=%%i 

set email_subject=New SVN Commit. (Author:%svn_author%, Message:%svn_log%)

echo.  >> %OutputFile%
echo Author:          %svn_author% >> %OutputFile%
echo Commit Time:     %svn_date% >> %OutputFile%

echo.  >> %OutputFile%
echo Message:  >> %OutputFile%
svnlook log %REPOS% -r %REV% >> %OutputFile%

echo.  >> %OutputFile%
echo Changed Files:  >> %OutputFile%
svnlook changed %REPOS% -r %REV% >> %OutputFile%
echo *********************************************************************************************************** >> %OutputFile%
REM echo *********************************************************************************************************** >> %OutputFile%

echo.  >> %OutputFile%
echo Diff Result:      >> %OutputFile%
svnlook diff %REPOS% -r %REV% >> %OutputFile%
echo *********************************************************************************************************** >> %OutputFile%
REM echo *********************************************************************************************************** >> %OutputFile%
REM mailer.py commit "$REPOS" "$REV" /path/to/mailer.conf

cd ./Email
EmailSender.py %svn_author% %REPOS% %REV% .