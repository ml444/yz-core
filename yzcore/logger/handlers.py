#!/usr/bin/env python3.5+
# -*- coding: utf-8 -*-
"""
@auth: cml
@date: 2019-07-10
@desc: 日志对象的处理函数

内置处理器
logging模块提供了一些处理器，可以通过各种方式处理日志消息。使用addHandler()方法将这些处理器添加给Logger对象。另外还可以为每个处理器配置它自己的筛选和级别。
logging.StreamHandler 可以向类似与sys.stdout或者sys.stderr的任何文件对象(file object)输出信息
logging.FileHandler 将日志消息写入文件filename。
logging.handlers.DatagramHandler(host，port) 发送日志消息给位于制定host和port上的UDP服务器。使用UDP协议，将日志信息发送到网络
logging.handlers.HTTPHandler(host, url) 使用HTTP的GET或POST方法将日志消息上传到一台HTTP 服务器。
logging.handlers.RotatingFileHandler(filename) 将日志消息写入文件filename。如果文件的大小超出maxBytes制定的值，那么它将被备份为filenamel。
logging.handlers.SocketHandler 使用TCP协议，将日志信息发送到网络。
logging.handlers.SysLogHandler 日志输出到syslog
logging.handlers.NTEventLogHandler 远程输出日志到Windows NT/2000/XP的事件日志
logging.handlers.SMTPHandler 远程输出日志到邮件地址
logging.handlers.MemoryHandler 日志输出到内存中的制定buffer
"""
from logging import StreamHandler, FileHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, SMTPHandler
import fcntl, time, os, codecs, string, re, types, pickle, struct, shutil
from stat import ST_DEV, ST_INO, ST_MTIME


class StreamHandlerMP(StreamHandler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a stream. Use for multiprocess.
    """

    def emit(self, record):
        """
        Emit a record.
        First seek the end of file for multiprocess to log to the same file
        寻找文件结尾以供多进程登录到同一文件
        """
        try:
            if hasattr(self.stream, "seek"):
                self.stream.seek(0, os.SEEK_END)
        except IOError as e:
            pass

        StreamHandler.emit(self, record)


class FileHandlerMP(FileHandler, StreamHandlerMP):
    """
    A handler class which writes formatted logging records to disk files
        for multiprocess
    """

    def emit(self, record):
        """
        Emit a record.

        If the stream was not opened because 'delay' was specified in the
        constructor, open it before calling the superclass's emit.
        如果由于在构造函数中指定了“delay”而未打开流，请在调用超类的emit之前将其打开。
        """
        if self.stream is None:
            self.stream = self._open()
        StreamHandlerMP.emit(self, record)


class RotatingFileHandlerMP(RotatingFileHandler, FileHandlerMP):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size.

    Based on logging.RotatingFileHandler, modified for Multiprocess
    """
    _lock_dir = '.lock'
    if os.path.exists(_lock_dir):
        pass
    else:
        os.mkdir(_lock_dir)

    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        For multiprocess, we use shutil.copy instead of rename.
        """

        self.stream.close()
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = "%s.%d" % (self.baseFilename, i)
                dfn = "%s.%d" % (self.baseFilename, i + 1)
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    shutil.copy(sfn, dfn)
            dfn = self.baseFilename + ".1"
            if os.path.exists(dfn):
                os.remove(dfn)
            if os.path.exists(self.baseFilename):
                shutil.copy(self.baseFilename, dfn)
        self.mode = 'w'
        self.stream = self._open()

    def emit(self, record):
        """
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().

        For multiprocess, we use file lock. Any better method ?
        """
        try:
            if self.shouldRollover(record):
                self.doRollover()
            FileLock = self._lock_dir + '/' + os.path.basename(self.baseFilename) + '.' + record.levelname
            f = open(FileLock, "w+")
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            FileHandlerMP.emit(self, record)
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            f.close()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class TimedRotatingFileHandlerMP(TimedRotatingFileHandler, FileHandlerMP):
    """
    Handler for logging to a file, rotating the log file at certain timed
    intervals.

    If backupCount is > 0, when rollover is done, no more than backupCount
    files are kept - the oldest ones are deleted.
    """
    _lock_dir = '.lock'
    if os.path.exists(_lock_dir):
        pass
    else:
        os.mkdir(_lock_dir)

    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=0, utc=0):
        FileHandlerMP.__init__(self, filename, 'a', encoding, delay)
        self.encoding = encoding
        self.when = when.upper()
        self.backupCount = backupCount
        self.utc = utc
        # Calculate the real rollover interval, which is just the number of
        # seconds between rollovers.  Also set the filename suffix used when
        # a rollover occurs.  Current 'when' events supported:
        # S - Seconds
        # M - Minutes
        # H - Hours
        # D - Days
        # midnight - roll over at midnight
        # W{0-6} - roll over on a certain day; 0 - Monday
        #
        # Case of the 'when' specifier is not important; lower or upper case
        # will work.
        if self.when == 'S':
            self.suffix = "%Y-%m-%d_%H-%M-%S"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$"
        elif self.when == 'M':
            self.suffix = "%Y-%m-%d_%H-%M"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}$"
        elif self.when == 'H':
            self.suffix = "%Y-%m-%d_%H"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}$"
        elif self.when == 'D' or self.when == 'MIDNIGHT':
            self.suffix = "%Y-%m-%d"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}$"
        elif self.when.startswith('W'):
            if len(self.when) != 2:
                raise ValueError("You must specify a day for weekly rollover from 0 to 6 (0 is Monday): %s" % self.when)
            if self.when[1] < '0' or self.when[1] > '6':
                raise ValueError("Invalid day specified for weekly rollover: %s" % self.when)
            self.dayOfWeek = int(self.when[1])
            self.suffix = "%Y-%m-%d"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}$"
        else:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)

        self.extMatch = re.compile(self.extMatch)

        if interval != 1:
            raise ValueError("Invalid rollover interval, must be 1")

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        record is not used, as we are just comparing times, but it is needed so
        the method signatures are the same
        """
        if not os.path.exists(self.baseFilename):
            # print "file don't exist"
            return 0

        cTime = time.localtime(time.time())
        mTime = time.localtime(os.stat(self.baseFilename)[ST_MTIME])
        if self.when == "S" and cTime[5] != mTime[5]:
            # print "cTime:", cTime[5], "mTime:", mTime[5]
            return 1
        elif self.when == 'M' and cTime[4] != mTime[4]:
            # print "cTime:", cTime[4], "mTime:", mTime[4]
            return 1
        elif self.when == 'H' and cTime[3] != mTime[3]:
            # print "cTime:", cTime[3], "mTime:", mTime[3]
            return 1
        elif (self.when == 'MIDNIGHT' or self.when == 'D') and cTime[2] != mTime[2]:
            # print "cTime:", cTime[2], "mTime:", mTime[2]
            return 1
        elif self.when == 'W' and cTime[1] != mTime[1]:
            # print "cTime:", cTime[1], "mTime:", mTime[1]
            return 1
        else:
            return 0

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.

        For multiprocess, we use shutil.copy instead of rename.
        """
        if self.stream:
            self.stream.close()
        # get the time that this sequence started at and make it a TimeTuple
        # t = self.rolloverAt - self.interval
        t = int(time.time())
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        if os.path.exists(dfn):
            os.remove(dfn)
        if os.path.exists(self.baseFilename):
            shutil.copy(self.baseFilename, dfn)
            # print "%s -> %s" % (self.baseFilename, dfn)
            # os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            # find the oldest log file and delete it
            # s = glob.glob(self.baseFilename + ".20*")
            # if len(s) > self.backupCount:
            #    s.sort()
            #    os.remove(s[0])
            for s in self.getFilesToDelete():
                os.remove(s)
        self.mode = 'w'
        self.stream = self._open()

    def emit(self, record):
        """
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().

        For multiprocess, we use file lock. Any better method ?
        """
        try:
            if self.shouldRollover(record):
                self.doRollover()
            FileLock = self._lock_dir + '/' + os.path.basename(self.baseFilename) + '.' + record.levelname
            f = open(FileLock, "w+")
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            FileHandlerMP.emit(self, record)
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            f.close()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
