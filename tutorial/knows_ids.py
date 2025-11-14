def main():
    known_ids_str = ";10101;10102;10103;10104;10105;10106;10107;10108;10109;10110;10111;10112"
    known_ids_set = set(known_ids_str.split(';'))
    known_ids_set.discard('')  # Remove any empty string that may result from leading semicolon

    data_lines = [
        "1000688170000008\t80940\t;10101;10102;10103;10104;10105;10106;10107;10108;10109;10110\t1\t26"
    ]

    for line in data_lines:
        parts = line.split('\t')
        if len(parts) < 3:
            continue
        reward_record_str = parts[2]
        reward_ids = reward_record_str.split(';')
        reward_ids = [id_str for id_str in reward_ids if id_str != '']  # Remove empty strings

        missing_ids = []
        for id_str in reward_ids:
            if id_str not in known_ids_set:
                missing_ids.append(id_str)

        print(f"Missing IDs in line: {missing_ids}")


if __name__ == "__main__":
    main()