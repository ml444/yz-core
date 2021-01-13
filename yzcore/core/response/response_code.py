# coding=utf-8
"""
    接口响应状态码
        1. 错误码的个位值与HTTP状态码的400～409有相关性，只有在被占用的情况下才顺移到下一个。
        2. 系统错误码取值范围500000～599999
        3. 业务错误码取值范围400000~-499999(分段使用)
"""
from enum import Enum, unique

__all__ = ("RegisterCode", "ErrorCode", "TipsCode", "WebsocketCode")

# 状态码注册,请同时添加注释
RegisterCode = [
    # 正常码
    200000,  # 正常,请求处理成功
    # 系统级错误代码
    500000,  # 服务器内部错误，无法完成请求
    500001,  # 服务器不支持请求的功能，无法完成请求
    500002,  # 无效的响应
    500003,  # 由于超载或系统维护，服务器暂时的无法处理客户端的请求
    500004,  # 服务器超时
    500005,  # HTTP协议的版本不支持
    500006,  # 兼容旧代码异常

    # 接口级错误代码
    400000,  # 请求语法或参数有误
    400001,  # 未认证
    400002,  # 
    400003,  # 请求太快
    400004,  # 找不到对象
    400005,  # 请求不允许
    400006,  # 请求不合理
    400007,  # 
    400008,  # 超时
    400009,  # 更新冲突
    400010,  # 资源已不存在


    ## 账号
    400100,  # 账号相关请求错误
    400101,  # 重复登录
    400103,  # 用户登录失败
    400104,  # 账号不存在
    400109,  # 更新信息失败
    400110,  # 手机号码格式不正确
    400111,  # 手机短信验证码错误
    400113,  # 60s内不能重复发送短信
    400118,  # 手机短信发送失败
    400119,  # 手机号码已被注册
    400120,  # email格式不正确
    400121,  # email验证码错误
    400123,  # 60s内不能重复发送邮件
    400126,  # 非邀请邮箱
    400127,  # 已经发送过邀请，请15分钟后再邀请
    400128,  # email发送失败
    400129,  # email已被注册
    400130,  # 
    400140,  # 密码格式不正确
    400141,  # 密码不一致
    400143,  # 密码错误
    400150,  # Token过期或失效

    ## 组织
    400200,  # 组织相关请求错误
    400209,  # 已切换到其他团队，请关闭当前页面
    400211,  # 用户未加入任何组织
    400212,  # 用户已加入该组织
    400213,  # 用户不属于此企业
    400223,  # 组织已存在
    400224,  # 组织不存在
    400229,  # 组织名称已被使用
    400233,  # 成员已存在
    400234,  # 成员不存在
    400239,  # 无法删除默认成员

    ## cms
    400300,  # node相关请求错误
    400301,  # 命名格式错误: 文件夹名字只支持中文, 数字, 字母或中划线, 且在50个字符以内
    400302,  # 命名重复
    400303,  # 文件夹已存在
    400304,  # 文件夹不存在
    400305,  # 最多只能创建四层文件夹
    400306,  # 文件已存在
    400307,  # 文件不存在
    400308,  # 请求超时
    400309,  # 
    400310,  # 标签名字格式错误: 字符长度在1-6内
    400311,  # 标签已存在
    400312,  # 标签不存在
    400313,  # 标签名字不能重复
    400314,  # 
    400320,  # 项目已存在
    400321,  # 项目不存在
    400322,  # 
    400323,  # 
    400324,  # 
    400330,  # 分组----------
    400331,  # 
    400332,  # 
    400340,  # 属性----------
    400341,  # 
    400342,  # 
    400343,  # 
    400380,  # limit超出限制
    400381,  # 搜索字段不存在
    400382,  # 排序字段不存在


    ## 权限
    400400,  # 权限相关请求错误
    400401,  # 权限不足
    400402,  # 权限创建失败
    400403,  # 
    400404,  # 找不到该权限
    400405,  # 
    400408,  # 权限查询超时

    ## editor
    400500,  # 编辑器相关请求错误
    400510,  # 模型名称不能超过50个字符
    400511,  # 模型描述不能超过100个字符
    400512,  # 模型组合不存在
    400513,  # 
    400514,  # 模型不存在
    400515,  # 
    400516,  # 
    400520,  # 材质库类型不存在
    400524,  # 材质不存在
    400525,  # 
    400530,  # 天空盒类型不存在
    400534,  # 天空盒不存在
    400540,  # 模板场景不存在
    400544,  # 场景不存在
    400550,  # 父级渲染对象不存在
    400554,  # 渲染对象不存在
    400560,  # 父级事件组不存在
    400564,  # 组件不存在
    400570,  # 父级资源不存在
    400573,  # 不支持的资源类型
    400574,  # 资源不存在
    400576,  # 资源内容不存在
    400584,  # 事件不存在

    ## 任务
    400600,  # Job相关请求错误
    400604,  # 任务不存在
    400608,  # 任务失败
    400610,  # 调用upload_policy参数有误
    400614,  # 对应upload_policy方法不存在
    400620,  # 调用cloud返回错误
    400630,  # 发布失败

    ## 应用
    400700,  # 应用相关请求错误
    400704,  # 应用不存在
    400710,  # platform不存在
    400720,  # 域名已经存在

    ## 支付
    400800,  # 支付相关请求错误
    
]


@unique
class ErrorCode(Enum):
    # 系统级错误代码
    UserNotLogin = dict(code=-10007, desc="用户尚未登录")
    RequestParamInvalid = dict(code=-10008, desc="参数json内容格式不正确")

    # 接口级错误代码
    UserNameAlreadyExists = dict(code=40001, desc="用户名已被注册")
    MaterialLibTypeNotExists = dict(code=40002, desc="材质库类型不存在")
    AccessPermissionDenied = dict(code=40003, desc="访问权限不足")
    SpaceNotExists = dict(code=40004, desc="空间不存在或已删除")
    FolderNameFormatInvalid = dict(
        code=40005, desc="文件夹名字格式错误: 文件夹名字只支持中文, 数字, 字母或下划线, 且在50个字符以内"
    )
    FolderNameConflict = dict(code=40006, desc="文件夹名字不能重复")
    FolderAlreadyExists = dict(code=40007, desc="文件夹已存在")
    FolderLevelLimited = dict(code=40008, desc="最多只能创建四层文件夹")
    DstDirFolderNotExists = dict(code=40009, desc="目标目录文件夹不存在")
    DirFolderNotExists = dict(code=40010, desc="当前目录文件夹不存在")
    FileNotExists = dict(code=40011, desc="文件不存在")
    FileNameConflict = dict(code=40012, desc="文件名字不能重复")
    FileNameFormatInvalid = dict(code=40013, desc="文件名字格式错误: 长度在1-50之间")
    CategoryTokenInvalid = dict(code=40014, desc="分类设置口令错误")
    CategoryParentPathNotExists = dict(code=40015, desc="分类父路径不存在")
    CategoryFormatInvalid = dict(code=40016, desc="分类名格式无效")
    TagNameFormatInvalid = dict(code=40017, desc="标签名字格式错误: 字符长度在1-6内")
    TagAlreadyExists = dict(code=40018, desc="标签已存在")
    TagNotExists = dict(code=40019, desc="标签不存在")
    TagNameConflict = dict(code=40020, desc="标签名字不能重复")
    TemplateNotExists = dict(code=40021, desc="空间自定义字段模板不存在")
    ModelNotExists = dict(code=40022, desc="模型不存在")
    AppCatalogNotExists = dict(code=40023, desc="目录方案不存在")
    CategoryAlreadyExists = dict(code=40024, desc="分类已存在")
    AppSpaceNotExists = dict(code=40025, desc="空间项目不存在")
    AppSolutionsNotFound = dict(code=40026, desc="app方案不存在")
    ProductionNotFound = dict(code=40027, desc="production不存在")
    PageSizeOverflow = dict(code=40028, desc="limit超出限制")
    CabinetNotFound = dict(code=40029, desc="cabinet不存在")
    OperationPermissionDenied = dict(code=40030, desc="未拥有此权限或操作权限不足")
    InvalidAccessToken = dict(code=40031, desc="invalid access token")
    UserNotFound = dict(code=40032, desc="用户不存在")
    ModelDescLengthOverflow = dict(code=40033, desc="模型描述不能超过100个字符")
    ModelNameLengthOverflow = dict(code=40034, desc="模型名称不能超过50个字符")
    CategoryNotExists = dict(code=40035, desc="分类不存在")
    ModelGroupNotExists = dict(code=40036, desc="模型组合不存在")
    ProductionNotExists = dict(code=40037, desc="production不存在")
    JobNotFound = dict(code=40038, desc="任务不存在")
    JobFailed = dict(code=40039, desc="任务失败")
    MaterialNotFound = dict(code=40040, desc="材质不存在")
    InvalidMobile = dict(code=40041, desc="手机号码格式不正确")
    InvalidOperationType = dict(code=40042, desc="非法操作类型")
    SmsSendFailed = dict(code=40043, desc="短信发送失败")
    CaptchaError = dict(code=40044, desc="验证码错误")
    InvalidUsernameOrPassword = dict(code=40045, desc="请输入正确的账号密码")
    PlatformNotFound = dict(code=40046, desc="platform不存在")
    WechatResponseError = dict(code=40047, desc="微信返回错误")
    SpaceNameAlreadyExists = dict(code=40048, desc="空间名称已被使用")
    InvalidEmail = dict(code=40049, desc="email格式不正确")
    InvalidUploadPolicy = dict(code=40050, desc="对应upload_policy方法不存在")
    InvalidPassword = dict(code=40051, desc="密码格式不正确")
    MobileAlreadyExists = dict(code=40052, desc="手机号码已注册")
    InvalidCabinetName = dict(code=40053, desc="cabinet名称格式不正确")
    CabinetNameAlreadyExisted = dict(code=40054, desc="cabinet名称已被使用")
    InvalidCallback = dict(code=40055, desc="invalid callback token")
    CallCloudError = dict(code=40056, desc="调用cloud返回错误")
    InvalidProductionName = dict(code=40057, desc="非法的产品名称")
    AppHomeCatalogNotExisted = dict(code=40058, desc="未设置首页方案")
    ClientNotFound = dict(code=40059, desc="客户端不存在")
    ClientChannelNotExists = dict(code=40060, desc="客户端渠道不存在")
    HomeSolutionsCannotDelete = dict(code=40061, desc="主页方案不能删除")
    InvalidRatio = dict(code=40062, desc="不正确的比例值")
    HostAlreadyExists = dict(code=40063, desc="域名已被使用")
    ProductNotFound = dict(code=40064, desc="产品不存在")
    SkyboxNotFound = dict(code=40065, desc="天空盒不存在")
    SkyboxLibTypeNotExists = dict(code=40066, desc="天空盒类型不存在")
    ApplicationNotExist = dict(code=40067, desc="应用不存在")
    UserLoginFailed = dict(code=40068, desc="用户登录失败")
    AccountUpdateFailed = dict(code=40069, desc="更新账号信息失败")
    SceneNotFound = dict(code=40070, desc="场景不存在")
    ParentEntityNotFound = dict(code=40071, desc="父级渲染对象不存在")
    EntityNotFound = dict(code=40072, desc='渲染对象不存在')
    ComponentNotFound = dict(code=40073, desc='组件不存在')
    ResourceNotFound = dict(code=40074, desc='资源不存在')
    ParentResourceNotFound = dict(code=40075, desc='父级资源不存在')
    TemplateSceneNotFound = dict(code=40076, desc='模板场景不存在')
    MediaNotFound = dict(code=40077, desc='资源内容不存在')
    EventNotFound = dict(code=40078, desc='事件不存在')
    ParentEventNotFound = dict(code=40079, desc='父级事件不存在')
    ModelIsNotPublic = dict(code=40080, desc='模型处于非公开状态')
    ModelIsLocked = dict(code=40081, desc='模型已被加密，请输入密码')
    ModelPasswordWrong = dict(code=40082, desc='模型密码错误')
    CollectionNotFound = dict(code=40083, desc='集合不存在')
    CollectionIsNotPublic = dict(code=40084, desc='集合未公开')
    CollectionIsLocked = dict(code=40085, desc='集合已被加密，请输入密码')
    CollectionPasswordWrong = dict(code=40086, desc='集合密码错误')
    TokenIsWrong = dict(code=40087, desc='Token过期或无效')
    NotInvitedEmail = dict(code=40088, desc='非邀请邮箱')
    RoleNotFound = dict(code=40089, desc='角色不存在')
    CannotDeleteDefaultRole = dict(code=40090, desc='无法删除默认角色')
    CatalogNotFound = dict(code=40091, desc='3D图册不存在')
    CorpNotFound = dict(code=40092, desc='企业不存在')
    RoleNameExist = dict(code=40093, desc='角色名已存在')
    UserIsInTeam = dict(code=40094, desc='用户已被邀请或已加入团队')
    UserNotInSpace = dict(code=40095, desc='未加入任何团队')
    InvitedEmailHasBeenSent = dict(code=40096, desc='已经发送过邀请，请15分钟后再邀请')
    ResetEmailHasBeenSent = dict(code=40097, desc='60s内不能重复发送邮件')
    TagNotFound = dict(code=40098, desc='标签不存在')
    UpdateUserInfoFail = dict(code=40099, desc='更新用户信息失败')
    DomainIsExist = dict(code=40100, desc='域名已经存在')
    UserNotInCorp = dict(code=40101, desc='用户不属于此企业')
    SearchFieldNotExist = dict(code=40102, desc='搜索字段不存在')
    SortFieldNotExist = dict(code=40103, desc='排序字段不存在')
    PublishFailed = dict(code=40104, desc='发布失败，服务器处理出错')
    EmailFormatError = dict(code=40105, desc='邮箱格式不正确')
    InstanceNotExists = dict(code=40106, desc='不存在对象')
    GroupNotExists = dict(code=40109, desc='群组不存在')
    SpaceIsChanged = dict(code=40110, desc='已切换到其他团队，请关闭当前页面')
    NoCorpSpace = dict(code=40111, desc='用户无企业空间')
    TypeNotSupport = dict(code=40112, desc='不支持的资源类型')
    ButtonNotFound = dict(code=40113, desc='按钮不存在')
    ProjectNotFound = dict(code=40114, desc='项目不存在')
    SceneNotInSameProject = dict(code=40115, desc='场景不在同一个项目')
    EventIsExist = dict(code=40116, desc='事件已存在')
    AccountNotExist = dict(code=40117, desc='账号不存在')
    CaptchaAlreadyExpired = dict(code=40118, desc='验证码已过期')
    TooManyRequest = dict(code=40119, desc='请求过于频繁')
    UserNotInvited = dict(code=40120, desc='您未被邀请加入，请联系系统管理员')
    ModelNumberNotEnough = dict(code=40121, desc='模型数量不足')
    ProjectlNumberNotEnough = dict(code=40122, desc='项目数量不足')
    UserAlreadyInvited = dict(code=40123, desc='用户已被邀请')
    UrlAlreadyExpired = dict(code=40124, desc='重置链接已过期')
    NotBeInvited = dict(code=40125, desc='未收到邀请或链接地址错误')
    PasswordErrorOverTimes = dict(code=40127, desc='错误次数超过5次，请明天再尝试')
    SpaceIsRemoved = dict(code=40128, desc='团队权限被删除')
    NeedCaptcha = dict(code=40129, desc='首次登陆需要验证码')
    MacAlreadyExist = dict(code=40130, desc='终端地址已存在')
    BeKickedOutFromTeam = dict(code=40131, desc='您已被移出团队，请联系管理员')
    UnauthorizedOrTimeout = dict(code=40132, desc='未授权或授权过期')
    UIPackInvalid = dict(code=40133, desc='UI数据包无效')
    UIIconPackInvalid = dict(code=40134, desc='ui icon 包无效')
    OnlyOnePageNotDelete = dict(code=40134, desc='只剩一个页面，不能删除')
    IconPackMustZip = dict(code=40134, desc='icon 包必须是zip格式压缩包')
    GetStaticResourceDataError = dict(code=40135, desc='服务器获取发布数据错误')
    NotFoundScenePublishData = dict(code=40135, desc='找不到场景发布数据')
    CapacityNotEnough = dict(code=40135, desc='容量不足')
    PasswordWrong = dict(code=40136, desc='密码错误')

    # 运营后台
    NotAuthenticatedUser = dict(code=-40001, desc='未认证用户，请重新登录')
    NotVisitedPermission = dict(code=-40002, desc='你没有访问权限')
    NotUpdatedPermission = dict(code=-40003, desc='你没有修改权限')
    PermissionDenied = dict(code=-40004, desc='你没有对应的操作权限权限')
    GroupDeleteFailedForManagerExisted = dict(code=-40005, desc='当前群组里有成员，不能删除当前群组')
    GroupNameExisted = dict(code=-40006, desc='当前群组名已经存在')
    PasswordNotSame = dict(code=-40007, desc='两次输入的密码不一致')
    HasExistsAccount = dict(code=-40008, desc='当前账号已存在')

    # 重新刷新页面
    NotSpaceReFlashPage = dict(code=-50001, desc='不存在空间，请刷新')


    # 兼容下-10000错误码的提示
    AttributeNameAlreadyExist = dict(code=-10000, desc='该属性名已经存在')
    DuplicateAttributeValue = dict(code=-10000, desc='属性值重复')
    FileCopyFailure = dict(code=-10000, desc='不能将文件复制到自身或其子目录下')
    FileMoveFailure = dict(code=-10000, desc='不能将文件移动到自身或其子目录下')
    FolderHasDeleteFileMoveOrCopyFailure = dict(code=-10000, desc='包含转换失败的文件，不能移动或者复制，请先删除转换失败的文件')
    FolderAlreadyExist = dict(code=-10000, desc='已经存在该文件夹')
    ParentFolderNotExist = dict(code=-10000, desc='父文件不存在')

    # 开放平台
    InvalidSpaceUserApiToken = dict(code=-70001, desc='无效的空间用户API token')
    SpaceNotAuthApplication = dict(code=-70002, desc='该用户空间未授权该应用')
    NotInternalSpaceAppUser = dict(code=-70003, desc='不是内部应用空间用户')
    AlreadyAddApplication = dict(code=-70004, desc='您已经添加了该应用')
    ApplicationNotPublishOrDeleted = dict(code=-70005, desc='应用未发布或被删除')
    ApplicationNotBelowCurrentSpace = dict(code=-70005, desc='该内部应用不属于当前空间')
    OpenServerError = dict(code=-70100, desc='open server invoke fail')

    CheckRepeat = dict(code=-99006, desc="重复登录错误")  # cml--> 重复登录


@unique
class EnErrorCode(Enum):
    # 英文版
    # 系统级错误代码
    UserNotLogin = dict(code=-10007, desc="User not logged in")
    RequestParamInvalid = dict(code=-10008, desc="Request param invalid")

    # 接口级错误代码
    UserNameAlreadyExists = dict(code=40001, desc="Username is already registered")
    MaterialLibTypeNotExists = dict(code=40002, desc="Material lib type not exists")
    AccessPermissionDenied = dict(code=40003, desc="Access permission denied")
    SpaceNotExists = dict(code=40004, desc="Space does not exist")
    DstDirFolderNotExists = dict(code=40009, desc="Destination directory folder does not exist")
    DirFolderNotExists = dict(code=40010, desc="Current directory folder does not exist")
    TagAlreadyExists = dict(code=40018, desc="Tag already exist")
    TagNotExists = dict(code=40019, desc="Tag dose noet exist")
    TemplateNotExists = dict(code=40021, desc="Space custom field template does not exist")
    ModelNotExists = dict(code=40022, desc="Model does not exist")
    ProductionNotFound = dict(code=40027, desc="Production dose not exist")
    PageSizeOverflow = dict(code=40028, desc="Exceeding the limit")
    CabinetNotFound = dict(code=40029, desc="Cabinet does not exist")
    OperationPermissionDenied = dict(code=40030, desc="Permission denied")
    InvalidAccessToken = dict(code=40031, desc="invalid access token")
    UserNotFound = dict(code=40032, desc="User does not exist")
    ModelDescLengthOverflow = dict(code=40033, desc="Model description cannot exceed 100 characters")
    ModelNameLengthOverflow = dict(code=40034, desc="Model name cannot exceed 50 characters")
    CategoryNotExists = dict(code=40035, desc="Category does not exist")
    ModelGroupNotExists = dict(code=40036, desc="Model combination does not exist")
    ProductionNotExists = dict(code=40037, desc="Production dose not exist")
    JobNotFound = dict(code=40038, desc="Job dose not exist")
    JobFailed = dict(code=40039, desc="Job failure")
    MaterialNotFound = dict(code=40040, desc="Material not found")
    InvalidMobile = dict(code=40041, desc="Invalid mobile")
    InvalidOperationType = dict(code=40042, desc="Invalid operation type")
    SmsSendFailed = dict(code=40043, desc="Sms send failed")
    CaptchaError = dict(code=40044, desc="Captcha error")
    InvalidUsernameOrPassword = dict(code=40045, desc="Invalid account or password")
    PlatformNotFound = dict(code=40046, desc="platform not found")
    WechatResponseError = dict(code=40047, desc="Wechat response error")
    SpaceNameAlreadyExists = dict(code=40048, desc="Space name Already exist")
    InvalidEmail = dict(code=40049, desc="Invalid email")
    InvalidUploadPolicy = dict(code=40050, desc="Invalid upload policy")
    InvalidPassword = dict(code=40051, desc="Invalid password")
    MobileAlreadyExists = dict(code=40052, desc="Mobile number registered")
    InvalidCabinetName = dict(code=40053, desc="Invalid cabinet name")
    CabinetNameAlreadyExisted = dict(code=40054, desc="Cabinet already existed")
    InvalidCallback = dict(code=40055, desc="invalid callback token")
    CallCloudError = dict(code=40056, desc="Call cloud error")
    InvalidProductionName = dict(code=40057, desc="Invalid production name")
    ClientNotFound = dict(code=40059, desc="Client not found")
    ClientChannelNotExists = dict(code=40060, desc="Client channel not found")
    InvalidRatio = dict(code=40062, desc="Invalid ratio")
    HostAlreadyExists = dict(code=40063, desc="Domain name is already in use")
    ProductNotFound = dict(code=40064, desc="Product not found")
    SkyboxNotFound = dict(code=40065, desc="Skybox not found")
    SkyboxLibTypeNotExists = dict(code=40066, desc="Skybox lib type not found")
    ApplicationNotExist = dict(code=40067, desc="Application not found")
    UserLoginFailed = dict(code=40068, desc="User login failed")
    AccountUpdateFailed = dict(code=40069, desc="Account update failed")
    SceneNotFound = dict(code=40070, desc="Scene not found")
    ParentEntityNotFound = dict(code=40071, desc="Parent entity not found")
    EntityNotFound = dict(code=40072, desc='Entity not found')
    ComponentNotFound = dict(code=40073, desc='Component not found')
    ResourceNotFound = dict(code=40074, desc='Resource not found')
    ParentResourceNotFound = dict(code=40075, desc='Parent resource not found')
    TemplateSceneNotFound = dict(code=40076, desc='Template scene not found')
    MediaNotFound = dict(code=40077, desc='Media not found')
    EventNotFound = dict(code=40078, desc='Event not found')
    ParentEventNotFound = dict(code=40079, desc='Parent event not found')
    ModelIsNotPublic = dict(code=40080, desc='Model is not public')
    ModelIsLocked = dict(code=40081, desc='Model is locked, please imput password')
    ModelPasswordWrong = dict(code=40082, desc='Model password wrong')
    CollectionNotFound = dict(code=40083, desc='Collection not found')
    CollectionIsNotPublic = dict(code=40084, desc='Collection is not public')
    CollectionIsLocked = dict(code=40085, desc='Collection is locked, please imput password')
    CollectionPasswordWrong = dict(code=40086, desc='Collection password wrong')
    TokenIsWrong = dict(code=40087, desc='Invalid token')
    NotInvitedEmail = dict(code=40088, desc='Non invitation email')
    RoleNotFound = dict(code=40089, desc='Role not found')
    CannotDeleteDefaultRole = dict(code=40090, desc='Cannot delete default role')
    CorpNotFound = dict(code=40092, desc='Enterprise does not exist')
    RoleNameExist = dict(code=40093, desc='Role name already exists')
    UserIsInTeam = dict(code=40094, desc='User has been invited or joined the team')
    UserNotInSpace = dict(code=40095, desc='User not joined team')
    InvitedEmailHasBeenSent = dict(code=40096, desc='Invitation has been sent, please invite again in 15 minutes')
    ResetEmailHasBeenSent = dict(code=40097, desc='Can not send mail repeatedly within 60s')
    TagNotFound = dict(code=40098, desc='Label does not exist')
    UpdateUserInfoFail = dict(code=40099, desc='Failed to update user information')
    DomainIsExist = dict(code=40100, desc='Domain name already exists')
    UserNotInCorp = dict(code=40101, desc='User does not belong to this enterprise')
    SearchFieldNotExist = dict(code=40102, desc='Search field does not exist')
    SortFieldNotExist = dict(code=40103, desc='Sort field does not exist')
    PublishFailed = dict(code=40104, desc='Publishing failed, server processing error')
    EmailFormatError = dict(code=40105, desc='Invalid email format')
    InstanceNotExists = dict(code=40106, desc='Object does not exist')
    GroupNotExists = dict(code=40109, desc='Group not exist')
    SpaceIsChanged = dict(code=40110, desc='Space is changed，please close the current page')
    TypeNotSupport = dict(code=40112, desc='The type not support')
    ButtonNotFound = dict(code=40113, desc='Button not found')
    ProjectNotFound = dict(code=40114, desc='Project not found')
    SceneNotInSameProject = dict(code=40115, desc='Scene not in same project')
    EventIsExist = dict(code=40116, desc='Event is exist')
    AccountNotExist = dict(code=40117, desc='Account dose not exist')
    CaptchaAlreadyExpired = dict(code=40118, desc='Captcha already expired')
    TooManyRequest = dict(code=40119, desc='Too many requests')
    UserNotInvited = dict(code=40120, desc='You are not invited to join, please contact your system administrator')
    ModelNumberNotEnough = dict(code=40121, desc='Model number not enouth')
    ProjectlNumberNotEnough = dict(code=40122, desc='Project number not enouth')
    UserAlreadyInvited = dict(code=40123, desc='User already invited')
    UrlAlreadyExpired = dict(code=40124, desc='Url already expired')
    NotBeInvited = dict(code=40125, desc='No invitation received or wrong link address')
    MacLimited = dict(code=40126, desc='The current device cannot enter the target space')
    PasswordErrorOverTimes = dict(code=40127, desc='Password more than 5 errors, please try again tomorrow')
    SpaceIsRemoved = dict(code=40128, desc='Space permissions deleted')
    NeedCaptcha = dict(code=40129, desc='First login requires verification code')
    MacAlreadyExist = dict(code=40130, desc='Terminal address already exists')
    BeKickedOutFromTeam = dict(code=40131, desc='You have been removed from the space. Please contact your system administrator')

    # 运营后台
    NotAuthenticatedUser = dict(code=-40001, desc='未认证用户，请重新登录')
    NotVisitedPermission = dict(code=-40002, desc='你没有访问权限')
    NotUpdatedPermission = dict(code=-40003, desc='你没有修改权限')
    PermissionDenied = dict(code=-40004, desc='你没有对应的操作权限权限')
    GroupDeleteFailedForManagerExisted = dict(code=-40005, desc='当前群组里有成员，不能删除当前群组')
    GroupNameExisted = dict(code=-40006, desc='当前群组名已经存在')
    PasswordNotSame = dict(code=-40007, desc='两次输入的密码不一致')
    HasExistsAccount = dict(code=-40008, desc='当前账号已存在')

    # 重新刷新页面
    NotSpaceReFlashPage = dict(code=-50001, desc='不存在空间，请刷新')
    NotInSpace = dict(code=-50001, desc='团队权限被删除')
    ClientMacLimited = dict(code=-50002, desc='终端无法访问')

    # 兼容下-10000错误码的提示
    AttributeNameAlreadyExist = dict(code=-10000, desc='Attribute name already eist')
    DuplicateAttributeValue = dict(code=-10000, desc='Duplicate attribute value')
    FileCopyFailure = dict(code=-10000, desc='Files cannot be copied to themselves or their subdirectories')
    FileMoveFailure = dict(code=-10000, desc='Files cannot be move to themselves or their subdirectories')
    DirHasDeleteFileMoveOrCopyFailure = dict(code=-10000,
                                             desc='The file containing the conversion failure cannot be moved or copied. Please delete the conversion failure file first')
    FolderAlreadyExist = dict(code=-10000, desc='Folder already exist')
    ParentFolderNotExist = dict(code=-10000, desc='Parent folder not exist')


    # 开放平台
    InvalidSpaceUserApiToken = dict(code=-70001, desc='无效的空间用户API token')
    SpaceNotAuthApplication = dict(code=-70002, desc='空间未授权该应用')
    NotInternalSpaceAppUser = dict(code=-70003, desc='不是内部应用空间用户')
    OpenServerError = dict(code=-70100, desc='open server invoke fail')

    CheckRepeat = dict(code=-99006, desc="Duplication error")  # cml--> 重复登录


@unique
class TipsCode(Enum):
    CheckUserName = dict(code=-99001, message="用户名错误")  # 用户名检查相关
    CheckMobile = dict(code=-99002, message="手机号码错误")  # 手机号码检查相关
    CheckPassword = dict(code=-99003, message="密码错误")  # 密码检查相关
    CheckParameter = dict(code=-99004, message="参数错误")  # 参数检查相关
    CheckCaptcha = dict(code=-99005, message="验证码错误")
    CheckRepeat = dict(code=-99006, message="重复登录错误")  # cml--> 重复登录

    PasswordNotSame = dict(code=40103, message='密码不一致')  # 密码不一致
    AccountAlreadyExists = dict(code=40104, message='已存在账户')  # 已存在账户
    GroupNotExists = dict(code=40105, message='群组不存在')  # 群组不存在
    InstanceNotExists = dict(code=40106, message="不存在对象")  # 不存在对象
    HasJoinGroup = dict(code=40106, message="已经加入该组")  # 已经加入该组
    RequiredParam = dict(code=40107, message="必填参数")  # 必填参数
    integerOutOfRange = dict(code=40108, message="整型数太大")  # 整型数太大
    ModelNotPublished = dict(code=40109, message='模型未发布')

    InviteNoPriceSet = dict(code=-30001, message="该空间当前没有购买任何套餐")
    InvitePriceSetOuttime = dict(code=-30002, message="该空间套餐已过期")
    InviteNoPriceSetItem = dict(code=-30003, message="该空间套餐不含邀请项")
    InviteOutPriceSetItemLimit = dict(code=-30004, message="该空间容量已满，请升级套餐")

    MeetingAlreadyOver = dict(code=-40001, message='会议已经结束')
    OutOfPeopleNum = dict(code=-40002, message='会议参与人数上限为10人，现在已经达到10人')
    ParticipantAlreadyDeleted = dict(code=-40003, message='您被会议管理人员移除会议，请联系会议发起人')
    NotInMeeting = dict(code=-40004, message='您未参加过此会议')
    MaxTwoReviewScene = dict(code=-40005, message='最多同时支持两个场景评审')
    MeetingNotOverYet = dict(code=-40006, message='会议尚未结束')


@unique
class EnTipsCode(Enum):
    CheckUserName = dict(code=-99001, message="Account error")  # 用户名检查相关
    CheckMobile = dict(code=-99002, message="Wrong mobile number")  # 手机号码检查相关
    CheckPassword = dict(code=-99003, message="Password error")  # 密码检查相关
    CheckParameter = dict(code=-99004, message="Parem error")  # 参数检查相关
    CheckCaptcha = dict(code=-99005, message="Captcha error")
    CheckRepeat = dict(code=-99006, message="Duplication error")  # cml--> 重复登录

    PasswordNotSame = dict(code=40103, message='Passwords are inconsistent')  # 密码不一致
    AccountAlreadyExists = dict(code=40104, message='Account already exist')  # 已存在账户
    GroupNotExists = dict(code=40105, message='Group does not exist')  # 群组不存在
    InstanceNotExists = dict(code=40106, message="Object does not exist")  # 不存在对象
    HasJoinGroup = dict(code=40106, message="Already joined the group")  # 已经加入该组
    RequiredParam = dict(code=40107, message="Required param")  # 必填参数
    integerOutOfRange = dict(code=40108, message="Integer too large")  # 整型数太大
    ModelNotPublished = dict(code=40109, message='Model not published')

    InviteNoPriceSet = dict(code=-30001, message="No packages are currently purchased for this space")
    InvitePriceSetOuttime = dict(code=-30002, message="The space package has expired")
    InviteNoPriceSetItem = dict(code=-30003, message="The space package does not include invitations")
    InviteOutPriceSetItemLimit = dict(code=-30004, message="This space is full, please upgrade the package")

    MeetingAlreadyOver = dict(code=-40001, message='The meeting is over')
    OutOfPeopleNum = dict(code=-40002, message='The maximum number of participants in the meeting is 10, now it has reached 10')
    ParticipantAlreadyDeleted = dict(code=-40003, message='You have been removed from the meeting by the meeting management. Please contact the meeting sponsor')
    NotInMeeting = dict(code=-40004, message='You have not attended this meeting')
    MaxTwoReviewScene = dict(code=-40005, message='Up to two scenario reviews are supported at the same time')
    MeetingNotOverYet = dict(code=-40006, message='The meeting is not over')


class WebsocketCode:

    def __init__(self, **kwargs):
        username = kwargs.get('username')
        data = kwargs.get('data', {})
        subject_name = kwargs.get('subject_name')
        object_name = kwargs.get('object_name')
        team_name = kwargs.get('team_name')
        self.JoinTwoMeeting = dict(code=-1001,
                                   message='您在其他地方加入了会议',
                                   data=dict(content=dict(zh='您在其他地方加入了会议',
                                                          en='You have joined another meeting')))
        self.DeletedParticipant = dict(code=-1002,
                                       message='{username}被移出会议'.format(username=username),
                                       data=dict(username=username,
                                                 content=dict(zh='被移出会议',
                                                              en='is removed from the meeting'),
                                                 participant_uid=data.get('uid')))
        self.ParticipantExit = dict(code=-1003,
                                    message='{username}已退出会议'.format(username=username),
                                    data=dict(username=username,
                                              content=dict(zh='已退出会议',
                                                           en='has left the meeting')))
        self.BeKickedOutFromTeam = dict(code=-1004,
                                        message='你已被管理员移出 {team_name} 团队'.format(team_name=team_name),
                                        data=dict(team_name=team_name,
                                                  content=dict(zh='你已被管理员移出团队',
                                                               en='You have been removed from the team by the administrator')))
        # self.DataUpdated = dict(code=1000, message='data updated', data=data)
        self.MasterChanged = dict(code=1001,
                                  message='{subject_name}已将主控权移交给{object_name}'.format(subject_name=subject_name, object_name=object_name),
                                  data=dict(subject_name=subject_name,
                                            object_name=object_name,
                                            content=dict(zh='已将主控权移交给',
                                                         en='has transferred the mastership to'),
                                            master_uid=data.get('master_uid')))
        self.JoinMeeting = dict(code=1002,
                                message='{username}已加入会议'.format(username=username),
                                data=dict(username=username,
                                          content=dict(zh='已加入会议',
                                                       en='has joined the meeting')))
        self.CreateMarker = dict(code=1003, message='create marker', data=data)
        self.DeleteMarker = dict(code=1004, message='delete marker', data=data)
        self.UpdateMakrer = dict(code=1005, message='update makrer', data=data)
        self.CreateReviewScene = dict(code=1006, message='create review scene', data=data)
        self.DeleteReviewScene = dict(code=1007, message='delete review scene', data=data)
        self.EndMeeting = dict(code=1008,
                               message='您已经结束会议',
                               data=dict(content=dict(zh='您已经结束会议',
                                                      en='You have ended the meeting')))
        self.MeetingAlreadyOver = dict(code=1009,
                                       message='会议已经结束',
                                       data=dict(content=dict(zh='会议已经结束',
                                                              en='The meeting is over')))

if __name__ == '__main__':
    print(ErrorCode.BeKickedOutFromTeam.value)