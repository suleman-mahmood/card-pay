"""
1. Get all closed loops
2. Get closed loop from closed loop id


2. Get user from user id
3. Get user from phone number
4. Get user from email
5. Get user from wallet id
6. Get all active users
7. Get all inactive users
8. Get all users of a user type


2. Get all users of a closed loop
4. Get all closed loops of a user
5. Get all active or inactive users of a closed loop
6. Get all unique identifiers of a closed loop (all roll numbers of LUMS)
user.closed_loops[closed_loop_id].unique_identifier


"""

def get_all_closed_loops(uow: AbstractUnitOfWork):
    """Get all closed loops"""
    with uow:
        sql = """
            select id, name, logo_url, description, regex, verification_type, created_at
            from closed_loops
            """ 
        uow.session.execute(sql)
        rows = uow.cursor.fetchall()
        closed_loops = []
        for row in rows:
            closed_loop = ClosedLoop(
                id=row[0],
                name=row[1],
                logo_url=row[2],
                description=row[3],
                regex=row[4],
                verification_type=row[5],
                created_at=row[6],
            )
            closed_loops.append(closed_loop)
        
        return closed_loops

def get_closed_loop_from_id(closed_loop_id:str, uow:AbstractUnitOfWork):

    with uow:
        closed_loop = uow.closed_loops.get(closed_loop_id=closed_loop_id)
    
    return closed_loop

def get_user_from_user_id(user_id:str, uow:AbstractUnitOfWork):
    
        with uow:
            user = uow.users.get(user_id=user_id)
        
        return user

def get_user_from_phone_number(phone_number: str, uow:AbstractUnitOfWork):
    with uow:
        sql = """
        select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at 
        from users 
        where phone_number = %s
        """

        self.cursor.execute(
            sql,
            [
                phone_number
            ]
        )

        row = self.cursor.fetchone()

        user = User(
            id=row[0], 
            personal_email=PersonalEmail(row[1]), 
            phone_number=PhoneNumber(row[2]), 
            user_type=UserType[row[3]], 
            pin=row[4], 
            full_name=row[5], 
            wallet_id=row[6],
            is_active=row[7], 
            is_phone_number_verified=row[8], 
            otp=row[9], 
            otp_generated_at=row[10], 
            location=Location(latitude=float(row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])), 
            created_at=row[12]
            )

        sql = """
        select user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at 
        from user_closed_loops 
        where user_id = %s
        """

        self.cursor.execute(
            sql,
            [
                user.id
            ]
        )

        rows = self.cursor.fetchall()

        for row in rows:
            closed_loop_user = ClosedLoopUser(
                closed_loop_id=row[1],
                unique_identifier=row[2], 
                id=row[3], 
                unique_identifier_otp=row[4], 
                status=row[5], 
                created_at=row[6]
            )

            user.closed_loops[row[1]] = closed_loop_user

        return user

def get_user_from_email(email: str, uow: AbstractUnitOfWork):
    with uow:
        sql = """
        select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at 
        from users 
        where personal_email = %s
        """

        self.cursor.execute(
            sql,
            [
                email
            ]
        )

        row = self.cursor.fetchone()

        user = User(
            id=row[0], 
            personal_email=PersonalEmail(row[1]), 
            phone_number=PhoneNumber(row[2]), 
            user_type=UserType[row[3]], 
            pin=row[4], 
            full_name=row[5], 
            wallet_id=row[6],
            is_active=row[7], 
            is_phone_number_verified=row[8], 
            otp=row[9], 
            otp_generated_at=row[10], 
            location=Location(latitude=float(row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])), 
            created_at=row[12]
            )

        sql = """
        select user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at 
        from user_closed_loops 
        where user_id = %s
        """

        self.cursor.execute(
            sql,
            [
                user.id
            ]
        )

        rows = self.cursor.fetchall()

        for row in rows:
            closed_loop_user = ClosedLoopUser(
                closed_loop_id=row[1],
                unique_identifier=row[2], 
                id=row[3], 
                unique_identifier_otp=row[4], 
                status=row[5], 
                created_at=row[6]
            )

            user.closed_loops[row[1]] = closed_loop_user

        return user

def get_user_from_wallet_id(wallet_id: str, uow: AbstractUnitOfWork):
    with uow:
        sql = """
        select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at 
        from users 
        where wallet_id = %s
        """

        self.cursor.execute(
            sql,
            [
                wallet_id
            ]
        )

        row = self.cursor.fetchone()

        user = User(
            id=row[0], 
            personal_email=PersonalEmail(row[1]), 
            phone_number=PhoneNumber(row[2]), 
            user_type=UserType[row[3]], 
            pin=row[4], 
            full_name=row[5], 
            wallet_id=row[6],
            is_active=row[7], 
            is_phone_number_verified=row[8], 
            otp=row[9], 
            otp_generated_at=row[10], 
            location=Location(latitude=float(row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])), 
            created_at=row[12]
            )

        sql = """
        select user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at 
        from user_closed_loops 
        where user_id = %s
        """

        self.cursor.execute(
            sql,
            [
                user.id
            ]
        )

        rows = self.cursor.fetchall()

        for row in rows:
            closed_loop_user = ClosedLoopUser(
                closed_loop_id=row[1],
                unique_identifier=row[2], 
                id=row[3], 
                unique_identifier_otp=row[4], 
                status=row[5], 
                created_at=row[6]
            )

            user.closed_loops[row[1]] = closed_loop_user

        return user

def get_all_active_or_inactive_users(status: bool,uow: AbstractUnitOfWork):
    with uow:
        sql = """
        select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at 
        from users 
        where is_actve = %s
        """
        uow.cursor.execute(
            sql,
            [
                status
            ]
        )

        rows = uow.cursor.fetchall()
        users = []

        for row in rows:
            user = User(
                id=row[0], 
                personal_email=PersonalEmail(row[1]), 
                phone_number=PhoneNumber(row[2]), 
                user_type=UserType[row[3]], 
                pin=row[4], 
                full_name=row[5], 
                wallet_id=row[6],
                is_active=row[7], 
                is_phone_number_verified=row[8], 
                otp=row[9], 
                otp_generated_at=row[10], 
                location=Location(latitude=float(row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])), 
                created_at=row[12]
                )

            sql = """
            select user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at 
            from user_closed_loops 
            where user_id = %s
            """

            uow.cursor.execute(
                sql,
                [
                    user.id
                ]
            )

            rows = uow.cursor.fetchall()

            for row in rows:
                closed_loop_user = ClosedLoopUser(
                    closed_loop_id=row[1],
                    unique_identifier=row[2], 
                    id=row[3], 
                    unique_identifier_otp=row[4], 
                    status=row[5], 
                    created_at=row[6]
                )

                user.closed_loops[row[1]] = closed_loop_user

            users.append(user)